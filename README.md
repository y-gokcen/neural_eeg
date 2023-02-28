# Neural complexity
A neural language model that computes various information-theoretic processing complexity measures (e.g., surprisal) for each word given the preceding context. Also, it can function as an adaptive language model ([van Schijndel and Linzen, 2018](http://aclweb.org/anthology/D18-1499)) which adapts to test domains.

**Note**: Recent updates remove dependencies but break compatibility with pre-2021 models. To use older models, use version 1.1.0: `git checkout tags/v1.1.0`

### Dependencies
Requires the following python packages (available through pip):
* [pytorch](https://pytorch.org/)

The following python packages are optional:
* progress
* dill (to handle binarized vocabularies)

### Quick Usage
The below all use GPUs. To use CPUs instead, omit the `--cuda` flag.

To train a Wikitext-2 LSTM model using GPUs:

    time python main.py --model_file 'wiki_2_model.pt' --vocab_file 'wiki_2_vocab.txt' --tied --cuda --data_dir './data/wikitext-2/' --trainfname 'train.txt' --validfname 'valid.txt'

To use that model to obtain incremental complexity estimates for the Wikitext-2 test partition:

    time python main.py --model_file 'wiki_2_model.pt' --vocab_file 'wiki_2_vocab.txt' --cuda --data_dir './data/wikitext-2/' --testfname 'test.txt' --test --words --nopp > FILENAME.OUTPUT

To instead use the trained model interactively:

    time python main.py --model_file 'wiki_2_model.pt' --vocab_file 'wiki_2_vocab.txt' --cuda --interact

### Quick Usage (Adaptative Language Modeling)
Take the above trained Wikitext-2 LSTM and adapt it to `adaptation_set.txt` in `data/adaptivecorpus`:

    time python main.py --model_file 'wiki_2_model.pt' --vocab_file 'wiki_2_vocab.txt' --cuda --data_dir './data/adaptivecorpus/' --testfname 'adaptation_set.txt' --test --words --adapt --adapted_model 'adapted_model.pt' > FILENAME.OUTPUT

To freeze the weights of the adaptive model and evaluate it on `heldout_set.txt` in `data/adaptivecorpus`:

    time python main.py --model_file 'adapted_model.pt' --vocab_file 'wiki_2_vocab.txt' --cuda --data_dir './data/adaptivecorpus/' --testfname 'heldout_set.txt' --test --words > FILENAME.OUTPUT

## Features
* Outputs incremental word-by-word information-theoretic complexity estimates (i.e. surprisal, entropy, entropy reduction) if the runtime command `--words` is given.
* Can function as an [adaptive language model](http://aclweb.org/anthology/D18-1499) if the runtime command `--adapt` is given (van Schijndel and Linzen, 2018). [Complete replication instructions](https://github.com/vansky/replications/blob/master/vanschijndel_linzen-2018-emnlp/vanschijndel_linzen-2018-emnlp-replication.md)
* Can operate interactively
* Early convergence detection (when validation loss does not increase for 3 epochs)
* Any words in the test corpus which were not seen during training are converted to `<unk>`. The probability of `<unk>` can be explicitly trained on `<unk>` tokens in the training data and/or implicitly learned using new words seen during validation.
* Can operate directly on gzipped corpora
* Does not require training data to be present at test time
* Can handle blank lines and unicode characters in the input corpora
* Can handle plaintext vocabularies (interpretable by humans, 1/3 the size, and only a few ms slower to load)

### Model parameters
These parameters help specify the model  

    --model {RNN_TANH, RNN_RELU, LSTM, GRU}: Uses the specified type of model (default: LSTM)  
    --emsize [INT]: The number of dimensions in the word embedding input layer (default: 200)  
    --nhid [INT]: The number of hidden units in each layer (default: 200)  
    --nlayers [INT]: The number of layers (default: 2)  
    --lr [FLOAT]: The learning rate; gradient is multiplied by this during weight updates (default: 20)  
    --clip [FLOAT]: Clips gradients to dampen large updates (default: 0.25)  
    --epochs [INT]: Maximum number of training epochs (default: 40)  
                    Training will stop early if the loss remains the same for three consecutive epochs  
    --batch_size [INT]: Number of parallel sequences to process simultaneously (default: 20)  
    --bptt [INT]: How far back in time to propagate error (default: 35)  
    --dropout [FLOAT]: Proportion of the network to drop out during training (default: 0.2)  
    --tied: If present, ties word embedding weights to output weights (default: absent)  
    --seed [INT]: Random seed (default: 1111)  
    --cuda: If present, uses GPUs/CUDA (default: absent)
    
### Data parameters
These parameters specify the data to use

    --model_file [PATH]: Path for saving/loading trained model (default: model.pt)
    --adapted_model [PATH]: Path for saving adapted model (default: adaptedmodel.pt)  
    --data_dir [PATH]: Directory of the corpus data (default: data/wikitext-2)  
    --vocab_file [PATH]: Path to store the training vocab (default: vocab.txt)
                         If the file has an extension of .bin the vocab will be binarized
    --trainfname [FILE]: Name of training file within the data directory (default: train.txt)  
    --validfname [FILE]: Name of validation file within the data directory (default: valid.txt)  
    --testfname [FILE]: Name of test file within the data directory (default: test.txt)  
    
### Runtime parameters
These parameters specify runtime options for using the model

    --test: If present, operate on test data; otherwise, train the model (default: absent)  
    --single: If present with --cuda, use only a single GPU even if more are present (default: absent)  

    --adapt: If present, adapt model weights during evaluation (default: absent)
             See van Schijndel and Linzen (2018) for details
    --interact: If present, load the model for interactive use (default: absent)  
    --view_layer [INT]: If 0 or greater, output the chosen hidden layer after each input word (default: -1)  
    
    --words: If present, output word-by-word complexity instead of sentence-level loss (default: absent)
    --log_interval [INT]: Number of batches between log outputs (default: 200)  
    --nopp: If present, suppress evaluation perplexity output (default: absent)  
    --nocheader: If present, suppress complexity header in output (default: absent)  
    --csep [CHAR]: Use specified character as separator for complexity output (default: ' ')  
    
    --guess: If present, display model's best guess(es) at each time step (default: absent)
    --guessn [INT]: Number of guesses for model to make at each time step (default: 1)  
    --guesssurps: If present, output guess surps along with each guess (default: absent)  
    --guessprobs: If present, output guess probabilities along with each guess (default: absent)  
    --complexn [INT]: Compute complexity over best N guesses instead of over full vocab (default: 0 aka full vocab)  

### Pre-trained models

This code should be compatible with pre-trained pytorch LSTMs (be sure to use `git checkout tags/v1.1.0`).
Here are a few different options depending on what you need (Email me if you'd like me to add your LSTM releases here):  
* 125 English Wiki LSTMs (2m,10m,20m,40m,80m tokens; 25 models each)  
 [van Schijndel et al (2019) "Quantity doesn’t buy quality syntax with neural language models"](https://www.aclweb.org/anthology/D19-1592)  
https://zenodo.org/record/3559340
* 5 models of Wiki English and 5 models of Spanish Wiki (80m tokens)  
[Davis and van Schijndel (2020) "RNN LMs Always Learn English-Like RC Attachment"](https://www.aclweb.org/anthology/2020.acl-main.179/)  
https://zenodo.org/record/3778994
* 5 models of discourse-intact English Wiki LSTMs (as opposed to the more standard isolated-sentence LSTMs found in most other releases; 80m tokens)  
[Davis and van Schijndel (2020) "Interaction with Context During RNN Sentence Processing"](https://psyarxiv.com/8r65d/)  
https://github.com/forrestdavis/GardenPath/tree/master/models/ordered
* 25 English Wiki and 25 English OpenWebText discourse-intact LSTMs  
[Davis and Altmann (2021) "Finding event structure in time: What recurrent neural networks can tell us about event structure in mind"](https://www.sciencedirect.com/science/article/abs/pii/S0010027721000706)  
https://zenodo.org/record/4053572
* 1 model for each of English, Hebrew, Russian, and Italian Wiki (80m tokens)  
[Gulordava et al (2018) "Colorless Green Recurrent Networks Dream Hierarchically"](https://www.aclweb.org/anthology/N18-1108/)  
https://github.com/facebookresearch/colorlessgreenRNNs/tree/master/data


### References

Marten van Schijndel and Tal Linzen. ["A Neural Model of Adaptation in Reading."](http://aclweb.org/anthology/D18-1499) In 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP 2018). 2018.
