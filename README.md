# ConvFinQA
The ConvFinQA dataset and code from EMNLP 2022 paper: 

ConvFinQA: Exploring the Chain of Numerical Reasoning in Conversational Finance Question Answering

<https://arxiv.org/abs/2210.03849>

## Requirements:

- pytorch 1.7.1
- huggingface transformers 4.4.2

## Dataset
We release the datasets in two formats - one for conversation level and the other for turn-level.
### Conversation level 
The following three files have entries for each full conversation:
```
train.json (3,037 examples)
dev.json (421 examples)
test.json (434 examples)
```

Each entry has the following fields:
```
General fields for all data:
"pre_text": the texts before the table;
"post_text": the text after the table;
"table": the table;
"id": unique example id. 
```
The "annotation" field contains the major information for the conversations. If the conversation is the Type I simple conversation, i.e., the decomposition from one FinQA question, then we have the following fields for "annotation" fields:
```
"annotation": {
  "original_program": original FinQA question;
  "dialogue_break": the conversation, as a list of question turns. 
  "turn_program": the ground truth program for each question, corresponding to the list in "dialogue_break".
  "qa_split": this field indicates the source of each question turn - 0 if from the decomposition of the first FinQA question, 1 if from the second. For the Type I simple conversations, this field is all 0s. 
  "exe_ans_list": the execution results of each question turn. 
}
```
Apart from "annotation" field, we also have the "qa" field for the original FinQA question. 

If the conversation is the Type II complex conversation, i.e., the decomposition from two FinQA questions, then "qa_split" field will have set of 0s first (turns from the first FinQA question), then followed by 1s (turns from the second FinQA question). We will also two fields "original_program_0" and "original_program_1" for the two original FinQA questions. 
Apart from "annotation" field, We have the "qa_0" and "qa_1" fields for the original two FinQA questions. 

### Turn level 
The following three files have entries for each conversation turn:
```
train_turn.json (11,104 examples)
dev_turn.json (1,490 examples)
test_turn.json (1,521 examples)
```
Apart from all the fields mentioned above, we have the following additional fields for each entry of these turn-level files:
```
"cur_program": the program for the current turn. 
"cur_dial": the list of questions up to the current turn.
"exe_ans": execution result of the current turn.
"cur_type": the type of current turn question, number selection or program.
"turn_ind": index of current turn.
"gold_ind": the set of supporting facts. 
```

## Leaderboard
For test set release, we only provide the input report and the conversations. To test the performance on test set, please submit your results to [Codalab](https://codalab.lisn.upsaclay.fr/competitions/8582

Prepare your prediction file into the following format, as a list of dictionaries, each dictionary contains two fields: the example id and the predicted program. The predicted program is a list of predicted program tokens with the 'EOF' as the last token. For example:
```
[
    {
        "id": "ETR/2016/page_23.pdf-2",
        "predicted": [
            "subtract(",
            "5829",
            "5735",
            ")",
            "EOF"
        ]
    },
    {
        "id": "INTC/2015/page_41.pdf-4",
        "predicted": [
            "divide(",
            "8.1",
            "56.0",
            ")",
            "EOF"
        ]
    },
    ...
]
```

## Code

### The retriever
Go to folder "finqanet_retriever".

#### Train
To train the retriever, edit config.py to set your own project and data path. Set "model_save_name" to the name of the folder you want to save the checkpoints. You can also set other parameters here. Then run:

```
sh run.sh
```

You can observe the dev performance to select the checkpoint. 

#### Inference
To run inference, edit config.py to change "mode" to "test", "saved_model_path" to the path of your selected checkpoint in the training, and "model_save_name" to the name of the folder to save the result files. Then run:

```
python Test.py
```

It will create an inference folder in the output directory and generate the files used for the program generator. 

To train the program generator in the next step, we need to get the retriever inference results for all the train, dev, and test files. Edit config.py to set "test_file" as the path to the train file, dev file, and test file respectively, also set "model_save_name" correspondingly, and run Test.py to generate the results for all 3 of them. 

### The generator
Go to folder "finqanet_generator".

#### Train
First we need to convert the results from the retriever to the files used for training. Edit the main entry in Convert.py to set the file paths to the retriever results path you specified in the previous step - for all 3 train, dev, and test files. To convert the training data, use the convert_train function; to convert dev and test file, use the convert_test file. 

Then run:

```
python Convert.py
```

to generate the train, dev, test files for the generator. 

Edit other parameters in config.py, like your project path, data path, the saved model name, etc. To train the generator, run:

```
sh run.sh
```

You can observe the dev performance to select the checkpoint. 

#### Inference
To run inference, edit config.py to change "mode" to "test", "saved_model_path" to the path of your selected checkpoint in the training, and "model_save_name" to the name of the folder to save the result files. Then run:

```
python Test.py
```

It will generate the result files in the created folder. 





## Citation
If you find this project useful, please cite it using the following format

```
@article{chen2022convfinqa,
  title={ConvFinQA: Exploring the Chain of Numerical Reasoning in Conversational Finance Question Answering},
  author={Chen, Zhiyu and Li, Shiyang and Smiley, Charese and Ma, Zhiqiang and Shah, Sameena and Wang, William Yang},
  journal={Proceedings of EMNLP 2022},
  year={2022}
}
```
