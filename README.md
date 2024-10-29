# gaze-control
**The project implements real-time gaze tracking by detecting facial landmarks using a convolutional neural network (CNN) built on TensorFlow. This allows users to control the interface with their eye movements.**

Here is a sample gif showing the detection result : 
![demo](https://github.com/user-attachments/assets/c4579b3b-fd3f-4e31-887b-d944dd22c77e)

## Installation
Just git clone this repo and you are good to go.
```bash
git clone https://github.com/yuetl3mr/gaze-control.git
```

## Usage

```bash
cd test
python test.py
```

## Train & evaluate

```bash
python3 landmark.py \
    --train_record=train.record \
    --val_record=validation.record \
    --batch_size=32 \
    --epochs=10
```
Training and testing files are required to be stored as TensorFlow Record files. 




