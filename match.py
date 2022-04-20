import matchzoo as mz
train_pack_raw = mz.datasets.wiki_qa.load_data('train', task='ranking')
dev_pack_raw = mz.datasets.wiki_qa.load_data('dev', task='ranking', filtered=True)
test_pack_raw = mz.datasets.wiki_qa.load_data('test', task='ranking', filtered=True)
preprocessor = mz.preprocessors.BasicPreprocessor(fixed_length_left=10, fixed_length_right=40, remove_stop_words=False)

train_pack_processed = preprocessor.fit_transform(train_pack_raw)
dev_pack_processed = preprocessor.transform(dev_pack_raw)
test_pack_processed = preprocessor.transform(test_pack_raw)

print(preprocessor.context)