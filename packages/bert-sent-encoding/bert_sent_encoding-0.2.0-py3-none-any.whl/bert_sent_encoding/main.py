from pytorch_pretrained_bert import BertTokenizer, BertModel
import re
import os
import json
import codecs

import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler

USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")


class InputExample(object):

	def __init__(self, unique_id, text_a, text_b):
		self.unique_id = unique_id
		self.text_a = text_a
		self.text_b = text_b


class InputFeatures(object):
	"""A single set of features of data."""

	def __init__(self, unique_id, tokens, input_ids, input_mask, input_type_ids):
		self.unique_id = unique_id
		self.tokens = tokens
		self.input_ids = input_ids
		self.input_mask = input_mask
		self.input_type_ids = input_type_ids


def convert_examples_to_features(examples, seq_length, tokenizer):
	"""Loads a data file into a list of `InputBatch`s."""

	features = []
	for (ex_index, example) in enumerate(examples):
		tokens_a = tokenizer.tokenize(example.text_a)

		tokens_b = None
		if example.text_b:
			tokens_b = tokenizer.tokenize(example.text_b)

		if tokens_b:
			# Modifies `tokens_a` and `tokens_b` in place so that the total
			# length is less than the specified length.
			# Account for [CLS], [SEP], [SEP] with "- 3"
			_truncate_seq_pair(tokens_a, tokens_b, seq_length - 3)
		else:
			# Account for [CLS] and [SEP] with "- 2"
			if len(tokens_a) > seq_length - 2:
				tokens_a = tokens_a[0:(seq_length - 2)]

		# The convention in BERT is:
		# (a) For sequence pairs:
		#  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
		#  type_ids: 0   0  0    0    0     0       0 0    1  1  1  1   1 1
		# (b) For single sequences:
		#  tokens:   [CLS] the dog is hairy . [SEP]
		#  type_ids: 0   0   0   0  0     0 0
		#
		# Where "type_ids" are used to indicate whether this is the first
		# sequence or the second sequence. The embedding vectors for `type=0` and
		# `type=1` were learned during pre-training and are added to the wordpiece
		# embedding vector (and position vector). This is not *strictly* necessary
		# since the [SEP] token unambigiously separates the sequences, but it makes
		# it easier for the model to learn the concept of sequences.
		#
		# For classification tasks, the first vector (corresponding to [CLS]) is
		# used as as the "sentence vector". Note that this only makes sense because
		# the entire model is fine-tuned.
		tokens = []
		input_type_ids = []
		tokens.append("[CLS]")
		input_type_ids.append(0)
		for token in tokens_a:
			tokens.append(token)
			input_type_ids.append(0)
		tokens.append("[SEP]")
		input_type_ids.append(0)

		if tokens_b:
			for token in tokens_b:
				tokens.append(token)
				input_type_ids.append(1)
			tokens.append("[SEP]")
			input_type_ids.append(1)

		input_ids = tokenizer.convert_tokens_to_ids(tokens)

		# The mask has 1 for real tokens and 0 for padding tokens. Only real
		# tokens are attended to.
		input_mask = [1] * len(input_ids)

		# Zero-pad up to the sequence length.
		while len(input_ids) < seq_length:
			input_ids.append(0)
			input_mask.append(0)
			input_type_ids.append(0)

		assert len(input_ids) == seq_length
		assert len(input_mask) == seq_length
		assert len(input_type_ids) == seq_length

		if ex_index < 5:
			pass

		features.append(
			InputFeatures(
				unique_id=example.unique_id,
				tokens=tokens,
				input_ids=input_ids,
				input_mask=input_mask,
				input_type_ids=input_type_ids))
	return features


def _truncate_seq_pair(tokens_a, tokens_b, max_length):
	"""Truncates a sequence pair in place to the maximum length."""

	# This is a simple heuristic which will always truncate the longer sequence
	# one token at a time. This makes more sense than truncating an equal percent
	# of tokens from each, since if one sequence is very short then each token
	# that's truncated likely contains more information than a longer sequence.
	while True:
		total_length = len(tokens_a) + len(tokens_b)
		if total_length <= max_length:
			break
		if len(tokens_a) > len(tokens_b):
			tokens_a.pop()
		else:
			tokens_b.pop()


def read_examples(lines):
	"""Read a list of `InputExample`s from an input file."""
	examples = []
	unique_id = 0
	for line in lines:
		line = line.strip()
		text_a = None
		text_b = None
		m = re.match(r"^(.*) \|\|\| (.*)$", line)
		if m is None:
			text_a = line
		else:
			text_a = m.group(1)
			text_b = m.group(2)
		examples.append(
			InputExample(unique_id=unique_id, text_a=text_a, text_b=text_b))
		unique_id += 1
	return examples


class bert_sent_encoding:
	def __init__(self, model_path, seq_length=64, batch_size=8):
		self.seq_length = seq_length
		self.batch_size = batch_size
		self.model_path = model_path
		# model_path = os.path.join(os.path.dirname(__file__), './model/chinese_L-12_H-768_A-12/')
		self.tokenizer = BertTokenizer.from_pretrained(model_path)
		self.model_bert = BertModel.from_pretrained(model_path)
		if torch.cuda.device_count() > 1:
			self.model_bert = torch.nn.DataParallel(self.model_bert)
		self.model_bert.to(device)
		self.model_bert.eval()

	def get_vector(self, texts, word_vector=False, layer=-1):
		if isinstance(texts, str):
			texts = [texts]

		examples = read_examples(texts)

		features = convert_examples_to_features(
			examples=examples, seq_length=self.seq_length, tokenizer=self.tokenizer)

		unique_id_to_feature = {}
		for feature in features:
			unique_id_to_feature[feature.unique_id] = feature

		all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
		all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
		all_example_index = torch.arange(all_input_ids.size(0), dtype=torch.long)

		eval_data = TensorDataset(all_input_ids, all_input_mask, all_example_index)
		eval_sampler = SequentialSampler(eval_data)
		eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=self.batch_size)

		vectors = []
		for input_ids, input_mask, example_indices in eval_dataloader:
			input_ids = input_ids.to(device)
			input_mask = input_mask.to(device)

			_, embedding = self.model_bert(input_ids, token_type_ids=None, attention_mask=input_mask)
			embedding = embedding.detach().cpu().numpy().tolist()
			vectors.extend(embedding)

		if len(vectors) == 1:
			vectors = vectors[0]
		return vectors

	def write_txt2vector(self, path_txt, path_vector, word_vector=False, layer=-1):
		with codecs.open(path_txt, 'r', encoding='utf-8') as f1:
			texts = [line.strip() for line in f1]
		vectors = self.get_vector(texts, word_vector, layer)
		with codecs.open(path_vector, 'w', encoding='utf-8') as f2:
			if len(vectors) == 768 and not isinstance(vectors[0], list):
				f2.write(json.dumps(vectors) + '\n')
			else:
				for vector in vectors:
					if len(vector) == 768 and not isinstance(vector[0], list):
						f2.write(json.dumps(vectors) + '\n')
					else:
						for v in vector:
							f2.write(json.dumps(v) + '\n')


if __name__ == '__main__':
	import json
	import time
	import numpy as np
	import sklearn
	from sklearn import metrics

	text = ['你吃饭了吗', 'php是最美的编程语言']
	start = time.time()
	bse = bert_sent_encoding(model_path='./model/chinese_L-12_H-768_A-12/')
	vectors = bse.get_vector(text)
	print('spend {}s'.format(time.time() - start))
	print(vectors[0] == vectors[1])
	print('type of vectors', type(vectors))
	msgreply = json.dumps({'text': text, 'vector': vectors}, ensure_ascii=False)
	print('type of msgregply', type(msgreply))
# print('msgreply', msgreply)

	vectors = np.array(vectors)
	print('cos sim', sklearn.metrics.pairwise.cosine_similarity(vectors[0:1, :], vectors[1:2, :]))
