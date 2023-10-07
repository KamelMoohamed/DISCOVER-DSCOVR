# DISCOVER-DSCOVR

### Challenge Summary

How to develop geomagnetic activity forecast using the raw DSCOVR data directly as input?


<img src="/static/source/challenge summary.png" />

### Solution Overview

<img src="/static/source/solution diagram.png" />

### Data Preprocessing
DSCOVR and WIND data are from different sources with different properties. To solve this, we followed these DSP methods:

<img src="/static/source/Nasa-data preprocessing.png" />

### Forecasting Model
Transformer model to extend the data for few hours later after the existing/available data

<img src="/static/source/forecasting diagram.png" />
Train Loss: 0.03 <br>
Validate loss: 0.06

<img src="/static/source/forecasting results.png" />

### Kp Prediction Model

We used bert-base-uncased, BERT model as a starter model and then we fine tuned it to serve our problem with less time 

Our model is pre-trained on similar time series problem.

We used the encoder only (self-supervised) to extract features from data.

Then we trained our own decoder on 5 months of data.

The final loss is 0.8 on MSE.

<img src="/static/source/transformer_arch.png" />




