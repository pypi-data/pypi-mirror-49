# coding=utf-8
#
# created by kpe on 28.Mar.2019 at 14:01
#

from __future__ import absolute_import, division, print_function

import os

import tensorflow as tf
import params

from bert.model import BertModelLayer


def map_from_stock_variale_name(name, prefix="bert"):
    name = name.split(":")[0]
    ns   = name.split("/")
    pns  = prefix.split("/")

    if ns[:len(pns)] != pns:
        return None

    name = "/".join(["bert"] + ns[len(pns):])
    ns = name.split("/")

    if ns[0] != "bert":
        return None
    if ns[1] not in ["encoder", "embeddings"]:
        return None
    if ns[1] == "embeddings":
        if ns[2] == "LayerNorm":
            return name
        else:
            return name + "/embeddings"
    if ns[1] == "encoder":
        if ns[3] == "intermediate":
            return "/".join(ns[:4] + ns[5:])
        else:
            return name
    return None


def map_to_stock_variable_name(name, prefix="bert"):
    name = name.split(":")[0]
    ns   = name.split("/")
    pns  = prefix.split("/")

    if ns[:len(pns)] != pns:
        return None

    name = "/".join(["bert"] + ns[len(pns):])
    ns   = name.split("/")

    if ns[1] not in ["encoder", "embeddings"]:
        return None
    if ns[1] == "embeddings":
        if ns[2] == "LayerNorm":
            return name
        else:
            return "/".join(ns[:-1])
    if ns[1] == "encoder":
        if ns[3] == "intermediate":
            return "/".join(ns[:4] + ["dense"] + ns[4:])
        else:
            return name
    return None


class StockBertConfig(params.Params):
    attention_probs_dropout_prob = None,  # 0.1
    hidden_act                   = None,  # "gelu"
    hidden_dropout_prob          = None,  # 0.1,
    hidden_size                  = None,  # 768,
    initializer_range            = None,  # 0.02,
    intermediate_size            = None,  # 3072,
    max_position_embeddings      = None,  # 512,
    num_attention_heads          = None,  # 12,
    num_hidden_layers            = None,  # 12,
    type_vocab_size              = None,  # 2,
    vocab_size                   = None,  # 30522

    def to_bert_model_layer_params(self):
        return map_stock_config_to_params(self)


def map_stock_config_to_params(bc):
    """
    Converts the original BERT config dictionary
    to a `BertModelLayer.Params` instance.
    :return: a `BertModelLayer.Params` instance.
    """
    bert_params = BertModelLayer.Params(
        num_layers=bc.num_hidden_layers,
        num_heads=bc.num_attention_heads,
        hidden_size=bc.hidden_size,
        hidden_dropout=bc.hidden_dropout_prob,
        attention_dropout=bc.attention_probs_dropout_prob,

        intermediate_size=bc.intermediate_size,
        intermediate_activation=bc.hidden_act,

        vocab_size=bc.vocab_size,
        use_token_type=True,
        use_position_embeddings=True,
        token_type_vocab_size=bc.type_vocab_size,
        max_position_embeddings=bc.max_position_embeddings,
    )
    return bert_params


def params_from_pretrained_ckpt(bert_ckpt_dir):
    bert_config_file = os.path.join(bert_ckpt_dir, "bert_config.json")

    with tf.io.gfile.GFile(bert_config_file, "r") as reader:
        bc = StockBertConfig.from_json_string(reader.read())
        bert_params = map_stock_config_to_params(bc)

    return bert_params


def load_stock_weights(bert: BertModelLayer, ckpt_file):
    assert isinstance(bert, BertModelLayer), "Expecting a BertModelLayer instance as first argument"
    assert tf.compat.v1.train.checkpoint_exists(ckpt_file), "Checkpoint does not exist: {}".format(ckpt_file)
    ckpt_reader = tf.train.load_checkpoint(ckpt_file)

    bert_prefix = bert.weights[0].name.split("/")[0]

    #
    # To set_weights() expects numpy arrays, so we
    # need to obtain numerical values for the weights
    # not present in the ckpt_file, when eager execution is not enabled.
    #
    if not tf.executing_eagerly():
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            weights = sess.run(bert.weights)
    else:
        weights = [weight.value() for weight in bert.weights]

    for ndx, (weight, model_weight) in enumerate(zip(weights, bert.weights)):
        stock_name = map_to_stock_variable_name(model_weight.name, bert_prefix)

        if ckpt_reader.has_tensor(stock_name):
            value = ckpt_reader.get_tensor(stock_name)
            weights[ndx] = value
        else:
            print("loader: No value for:[{}], i.e.:[{}] in:[{}]".format(model_weight.name, stock_name, ckpt_file))

    bert.set_weights(weights)
    print("Done loading {} BERT weights from: {} into {} (prefix:{})".format(
        len(weights), ckpt_file, bert, bert_prefix))
