# ConvFinQA
The ConvFinQA dataset and code from EMNLP 2022 paper: CONVFINQA: Exploring the Chain of Numerical Reasoning in Conversational Finance Question Answering

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
