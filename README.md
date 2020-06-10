# SocialVisTUM - An Interactive Graphical Toolkit to Visualize and Label Clusters of Social Media Texts

The method used to create aspect clusters is based on an existing approach that can be found here: [Unsupervised-Aspect-Extraction](https://github.com/ruidan/Unsupervised-Aspect-Extraction)

## Requirements
- Only a browser is required to test the tool with the existing data
- To test the toolkit with a new data set, Python 2.7 and a package manager like Conda are required.

## Test the Toolkit With Existing Data Using Github Pages
To test the toolkit with existing data, use the following links: 

- [SocialVisTum Demo with automatic labels](https://martinkirchhoff.github.io/SocialVisTum/visualization-demos/automatic-labels/index.html)
- [SocialVisTum Demo with manual labels (case study)](https://martinkirchhoff.github.io/SocialVisTum/visualization-demos/manual-labels/index.html)

## Tool Overview and Functionalities

### Tool Overview

#### Nodes
- Nodes represent aspect clusters
- Nodes are are automatically labeled with suitable names
- Next to the name, the number of occurrences can be seen (Number of sentences that refer to the aspects)
- The node size is based on the number of occurrences

#### Links
- Links and link labels represent the correlation between two aspects
- If the correlation is larger (in absolute terms), the line thickness increases

#### Force-Directed Graph Layout
- Nodes repel each other
- A gravitational force keeps the graph centered

### Tool Functionalities

#### Move Nodes
- Simply move aspect nodes by dragging the node or the associated label

#### Rename Nodes
- To rename a node, left-click on the label and input the new name
- If you download an updated JSON file this change will be reflected in the output

#### Remove Nodes
- To remove a node, right-click on its label

#### Sidebar Options
- *Occurrence threshold* defines the percentage of sentences that must refer to an aspect to display the associated node
- *Correlation threshold* defines the correlation required to display the associated link
- *Most similar words* displays representative words for an aspect after double-clicking the node
- *Most similar sentences* displays representative sentences for an aspect after double-clicking the node
- *Download updated data as JSON file* can be used to download an updated JSON file after renaming or deleting aspects
- *Center* can be used to move the graph position and the gravitational force
- *Link* can be used to change the length of links

##  Test the Toolkit With New Data or Parameters

1. Download the folder visualization-project from the repository.

2. Open a terminal window in the folder visualization-project.

3. Use ```conda env create -f environment.yml``` to create a new environment with the name *visualization_env*, which contains the required packages.

4. Activate the environment using ```source activate visualization_env```

5. Download the pre-trained GloVe embeddings with 6B tokens (glove.6B.zip) from [https://nlp.stanford.edu/projects/glove/](https://nlp.stanford.edu/projects/glove/)

6. Extract the zip and put the whole folder *glove.6B* into the folder *pretrained_embeddings*.

7. Navigate to the *datasets* folder and copy your dataset as a subfolder in the directory. The name of the subfolder will be used as &lt;domain&gt; of your dataset in the following commands.

8. To preprocess the data and finetune the embeddings go back to the main directory and use ```python ./code/preprocess.py --domain-name <domain>```  
The parameter &lt;domain&gt; specifies the name of the folder that includes the data set.   
If you want to use the existing organic food data set use *organic_food_preprocessed*.    

9. To train the model and extract all relevant aspect information, use ```python ./code/train.py --domain <domain> --conf <conf> --emb-path ./preprocessed_data/<domain>/glove_w2v_300_filtered.txt```
&lt;conf&gt; is used to create a separate result folder for each time you train the model with different parameters. You can simply use 0 for the first time. &lt;emb-path&gt; specifies the location of the finetuned embeddings.
Moreover, you can adjust all other relevant training parameters as explained in the *Training Parameter Overview*. The results are saved in the folder */code/output_dir/&lt;domain&gt;/&lt;conf&gt;*.

10. To show the visualization and labeling tool in the browser, use ```python ./code/display_visualization.py --domain <domain> --conf <conf> --port <port>```.  
&lt;port&gt; specifies the port where it is opened and is by default set to 9000.  
If the visualization does not show anything or the visualization shows the result of a previous setting, the port might already be in use. To get the correct result, simply use another port (e.g., 9001).

### Training Parameter Overview

The following table defines all the parameters that are used to train the model with new data. All the parameters can be adjusted by adding the name of the parameter and its associated value to the training command.   
Example: ```python ./code/train.py --domain organic_food_preprocessed --conf 0 --emb-path ./preprocessed_data/<domain>/glove_w2v_300_filtered.txt --num-topics 5 --num-words 30```

| Name                  | Explanation                                             | Type  | Default                            |
|-----------------------|---------------------------------------------------------|-------|------------------------------------|
| --domain              | Domain of the corpus                                    | str   | required                           |
| --conf                | Train configuration for the given domain                | str   | required                           |
| --emb-path            | Path to the word embedding file                         | str   | required                           |
| --num-topics          | Number of aspects/topics detected                               | int   | 20                                 |
| --vocab-size          | Vocabulary size. 0 means no limit                       | int   | 9000                               |
| --num-words           | Number of representative sentences displayed            | int   | 10                                 |
| --num-sentences       | Number of representative words displayed                | int   | 10                                 |
| --labeling-num-words  | Number of representative words used to generate labels  | int   | 25                                 |
| --batch-size          | Batch size used to train the model                      | int   | 64                                 |
| --epochs              | Number of epochs                                        | int   | 20                                 |
| --neg-size            | Number of negative instances used for training          | int   | 20                                 |
| --maxlen              | Maximum number of words in every sentence               | int   | 0 (Unlimited)                                 |
| --algorithm           | Optimization algorithm used (rmsprop, sgd, adam...)     | str   | "adam"                             |
| --fix-clusters        | Fix initial aspect clusters ("yes" or "no")              | str   |"no"                               |
| --ortho-reg           | Weight of orthogonal regularization                     | float | 0.1                                |
| --probability-batches | Number of batches used to calculate aspect probabilities | int   | Number of training examples /5000 |
| --emb-dim             | Embeddings dimension                                    | int   | 300                                |
