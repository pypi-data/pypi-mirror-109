import warnings
warnings.filterwarnings("ignore")
import random, pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,cohen_kappa_score,confusion_matrix,roc_curve,balanced_accuracy_score
import sys, copy
import pandas as pd
import numpy as np
import io, math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets,transforms
import torch.optim as optim
from torch.autograd import Variable
import matplotlib.pyplot as plt
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
import scikitplot as skplt
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from captum.attr import IntegratedGradients

def one_hot_smile(smile, smile_l = 75):
	key="()+–./-0123456789=#@$ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]abcdefghijklmnopqrstuvwxyz^"
	test_list=list(key)
	res = {val : idx  for idx, val in enumerate(test_list)}
	threshold=smile_l

	if len(smile)<=threshold:
		smile=smile+("^"*(threshold-len(smile)))
	else:
		smile=smile[0:threshold]
	array=[[0 for j in range(len(key))] for i in range(threshold)]
	for i in range(len(smile)):
		array[i][res[smile[i]]]=1
	array=torch.Tensor(array)

	return array

def one_hot_seq(seq, seq_l = 315):
	key="ABCDEFGHIJKLMNOPQRSTUVWXYZ^"
	seq=seq.upper()
	test_list=list(key)
	res = {val : idx  for idx, val in enumerate(test_list)}
	threshold=seq_l

	if len(seq)<=threshold:
		seq=seq+("^"*(threshold-len(seq)))
	else:
		seq=seq[0:threshold]
	array=[[0 for j in range(len(key))] for i in range(threshold)]
	for i in range(len(seq)):
	  array[i][res[seq[i]]]=1
	array=torch.Tensor(array)

	return array

class Attention(nn.Module):
	#Implementation of Attention Mechanism
    def __init__(self, device,hidden_size):
        super(Attention, self).__init__()
        
        self.device = device

        self.hidden_size = hidden_size

        self.concat_linear = nn.Linear(self.hidden_size * 2, self.hidden_size)

        self.attn = nn.Linear(self.hidden_size, hidden_size)

    def forward(self, rnn_outputs, final_hidden_state):
        batch_size, seq_len, _ = rnn_outputs.shape
        attn_weights = self.attn(rnn_outputs) # (batch_size, seq_len, hidden_dim)
        attn_weights = torch.bmm(attn_weights, final_hidden_state.unsqueeze(2))
        attn_weights = F.softmax(attn_weights.squeeze(2), dim=1)
        context = torch.bmm(rnn_outputs.transpose(1, 2), attn_weights.unsqueeze(2)).squeeze(2)
        attn_hidden = torch.tanh(self.concat_linear(torch.cat((context, final_hidden_state), dim=1)))
        return attn_hidden, attn_weights


class BLSTM(nn.Module):
  #BLSTM(77, smile_h, smile_l, smile_o, 27, seq_h, seq_l, seq_o, output_dim,device, batch_size=batch_size)
  def __init__(self, input_smile_dim, hidden_smile_dim, layer_smile_dim, smile_o, input_seq_dim, hidden_seq_dim, layer_seq_dim, seq_o, device,dropout=0.5, output_dim=2, batch_size=16):
    super(BLSTM, self).__init__()
    #Implementation of Attention based Bi-LSTM for sequences and smiles
    self.hidden_smile_dim = hidden_smile_dim
    self.layer_smile_dim = layer_smile_dim
    self.hidden_seq_dim = hidden_seq_dim
    self.layer_seq_dim = layer_seq_dim
    self.output_dim = output_dim
    self.num_smile_dir=2
    self.num_seq_dir=2
    self.device=device
    self.batch_size=batch_size

    self.lstm_smile = nn.LSTM(input_smile_dim, hidden_smile_dim, layer_smile_dim,bidirectional=True,batch_first=True)
    self.lstm_seq = nn.LSTM(input_seq_dim, hidden_seq_dim, layer_seq_dim,bidirectional=True,batch_first=True)
    self.dropout = nn.Dropout(dropout)

    self.attn_smile = Attention(self.device, self.hidden_smile_dim * self.num_smile_dir)
    self.attn_seq = Attention(self.device, self.hidden_seq_dim * self.num_seq_dir)

    self.fc_seq_att= nn.Linear(hidden_seq_dim*self.num_seq_dir,50)

    self.fc_smile_att= nn.Linear(hidden_smile_dim*self.num_smile_dir,50)
    
    self.batch_norm_combined = nn.BatchNorm1d(smile_o+seq_o, affine = False)
    self.fc_combined = nn.Sequential(nn.Linear(100,10),nn.ReLU(),nn.Linear(10,output_dim))
		
  def forward(self, x1,x2):
    out_smile, (hn_smile, cn_smile) = self.lstm_smile(x1)
    out_seq, (hn_seq, cn_seq) = self.lstm_seq(x2)
    #Apply attention
    # For smiles
    # take the output as X_smile which we were using out_s mile
    batch_size=out_smile.shape[0]
    final_state_smile = hn_smile.view(self.layer_smile_dim, self.num_smile_dir, batch_size, self.hidden_smile_dim)[-1]
        
    final_hidden_state_smile = None
    
    if self.num_smile_dir == 1:
        final_hidden_state_smile = final_state_smile.squeeze(0)
    elif self.num_smile_dir == 2:
        h_1_smile, h_2_smile = final_state_smile[0], final_state_smile[1]
        final_hidden_state_smile = torch.cat((h_1_smile, h_2_smile), 1)  
    # For seq
    # take the output as X_seq which we were using out_seq 
    final_state_seq = hn_seq.view(self.layer_seq_dim, self.num_seq_dir, batch_size, self.hidden_seq_dim)[-1]
        
    final_hidden_state_seq = None
    
    if self.num_seq_dir == 1:
        final_hidden_state_seq = final_state_seq.squeeze(0)
    elif self.num_seq_dir == 2:
        h_1_seq, h_2_seq = final_state_seq[0], final_state_seq[1]
        final_hidden_state_seq = torch.cat((h_1_seq, h_2_seq), 1)  

    attn_weights_smile = None
    
    X_smile, attn_weights_smile = self.attn_smile(out_smile, final_hidden_state_smile)
    
    attn_weights_seq = None
    
    X_seq, attn_weights_seq = self.attn_seq(out_seq, final_hidden_state_seq)
    
    #Attention calculated, now use this in FC layers.
    out_smile=X_smile
    out_seq=X_seq
    out_smile = self.dropout(out_smile)
    out_seq = self.dropout(out_seq)
    out_seq=self.fc_seq_att(out_seq.view(-1,self.hidden_seq_dim*self.num_seq_dir))
    out_seq = self.dropout(out_seq)
    out_smile=self.fc_smile_att(out_smile.view(-1,self.hidden_smile_dim*self.num_smile_dir))
    out_smile = self.dropout(out_smile)

    out_combined=torch.cat((out_smile,out_seq), dim=1)
    out_combined=self.fc_combined(out_combined)
    prob=nn.Softmax(dim=1)(out_combined)
    pred=nn.LogSoftmax(dim=1)(out_combined)

    return pred

def check_accuracy_per_epoch(model,x_smile,x_seq,y_model, epoch_wise, epochno,  device, batch_size=16):
	num_correct = 0
	num_samples = 0
	model.eval()
	count=1
	num_pred=[]
	num_prob=[]

	with torch.no_grad():
		for beg_i in range(0, x_smile.shape[0], batch_size):
			x_smile_batch = x_smile[beg_i:beg_i + batch_size]
			x_seq_batch = x_seq[beg_i:beg_i + batch_size]
			y_batch = y_model[beg_i:beg_i + batch_size]
			x_smile_batch=torch.FloatTensor(x_smile_batch)
			x_seq_batch=torch.FloatTensor(x_seq_batch)
			y_batch = y_batch.to(dtype=torch.long)
            #y_batch=torch.LongTensor(list(y_batch))
			x_smile_batch = Variable(x_smile_batch)
			x_seq_batch = Variable(x_seq_batch)
			y_batch = Variable(y_batch)

			x_smile_batch=x_smile_batch.to(device)
			x_seq_batch=x_seq_batch.to(device)
			y_batch=y_batch.to(device)

			scores = model(x_smile_batch,x_seq_batch)
   
			_, predictions = scores.max(1)
			#probs = [i[1].item() for i in scores[1]]
			num_pred.extend(predictions.tolist())
			#num_prob.extend(probs)
			num_correct += (predictions == y_batch).sum()
			num_samples += predictions.size(0)
			count+=1
		
		y_model=torch.Tensor.cpu(y_model)


		accuracy=accuracy_score(np.array(y_model),np.array(num_pred))
		precision=precision_score(np.array(y_model),np.array(num_pred))
		recall=recall_score(np.array(y_model),np.array(num_pred))
		f1=f1_score(np.array(y_model),np.array(num_pred))
		roc=roc_auc_score(np.array(y_model),np.array(num_pred))
		kappa=cohen_kappa_score(np.array(y_model),np.array(num_pred))
		conf_matrix=confusion_matrix(np.array(y_model),np.array(num_pred))
		bal_acc=balanced_accuracy_score(np.array(y_model),np.array(num_pred))


		epoch_wise[epochno]=[accuracy,precision,recall, kappa, bal_acc, f1, roc, conf_matrix]

				
def train_epoch(model,x_train_smile,x_train_seq,y_train,x_test_smile,x_test_seq,y_test,train_epochwise,test_epochwise, epochno, optimizer, criterion, device, batch_size=16):
    model.train()
    loss_train_array = []
    for beg_i in range(0, x_train_smile.shape[0], batch_size):
        x_train_smile_batch = x_train_smile[beg_i:beg_i + batch_size]
        x_train_seq_batch = x_train_seq[beg_i:beg_i + batch_size]
        y_train_batch = y_train[beg_i:beg_i + batch_size]
        x_train_smile_batch=list(x_train_smile_batch)
        x_train_seq_batch=list(x_train_seq_batch)
        x_train_smile_batch=torch.stack(x_train_smile_batch)
        x_train_smile_batch=torch.FloatTensor(x_train_smile_batch)
        x_train_seq_batch=torch.stack(x_train_seq_batch)
        x_train_seq_batch=torch.FloatTensor(x_train_seq_batch)
        y_train_batch = y_train_batch.to(dtype=torch.long)
        #y_train_batch=torch.LongTensor(list(y_train_batch))
        
        x_train_smile_batch = Variable(x_train_smile_batch)
        x_train_seq_batch = Variable(x_train_seq_batch)
        y_train_batch = Variable(y_train_batch)
 
        x_train_smile_batch=x_train_smile_batch.to(device)
        x_train_seq_batch=x_train_seq_batch.to(device)
        y_train_batch=y_train_batch.to(device)
 
        optimizer.zero_grad()
        # (1) Forward
        y_comb_train = model(x_train_smile_batch,x_train_seq_batch)
        y_hat_train=y_comb_train
        # y_hat_train= model(x_train_smile_batch,x_train_seq_batch)
        # (2) Compute diff
        loss_train = criterion(y_hat_train, y_train_batch)
        # (3) Compute gradients
        loss_train.backward()
        # (4) update weights
        optimizer.step()        
        loss_train_array.append(torch.Tensor.cpu(loss_train).data.numpy())
    
    check_accuracy_per_epoch(model,x_train_smile,x_train_seq,y_train, train_epochwise, epochno,  device, batch_size=batch_size)
    
    loss_test=0
    loss_test_array=[]
 
    for beg_i in range(0, x_test_smile.shape[0], batch_size):
 
        x_test_smile_batch = x_test_smile[beg_i:beg_i + batch_size]
        x_test_seq_batch = x_test_seq[beg_i:beg_i + batch_size]
        y_test_batch = y_test[beg_i:beg_i + batch_size]
        x_test_smile_batch=list(x_test_smile_batch)
        x_test_smile_batch=torch.stack(x_test_smile_batch)
        x_test_smile_batch=torch.FloatTensor(x_test_smile_batch)
        x_test_seq_batch=list(x_test_seq_batch)
        x_test_seq_batch=torch.stack(x_test_seq_batch)
        x_test_seq_batch=torch.FloatTensor(x_test_seq_batch)
        y_test_batch = y_test_batch.to(dtype=torch.long)
        #y_test_batch=torch.LongTensor(list(y_test_batch))
        x_test_smile_batch = Variable(x_test_smile_batch)
        x_test_seq_batch = Variable(x_test_seq_batch)
        y_test_batch = Variable(y_test_batch)
 
        x_test_smile_batch=x_test_smile_batch.to(device)
        x_test_seq_batch=x_test_seq_batch.to(device)
        y_test_batch=y_test_batch.to(device)
 
        # (1) Forward
        y_comb_test = model(x_test_smile_batch,x_test_seq_batch)
        y_hat_test= y_comb_test
        # y_hat_test= model(x_test_smile_batch,x_test_seq_batch)
        # (2) Compute diff
        loss_test = criterion(y_hat_test, y_test_batch)
        loss_test_array.append(loss_test.to(device))

    val_loss=sum(loss_test_array)/len(loss_test_array)
    train_loss=sum(loss_train_array)/len(loss_train_array)
    check_accuracy_per_epoch(model,x_test_smile,x_test_seq,y_test, test_epochwise, epochno, device, batch_size = batch_size)
    print("Training loss is", train_loss)
    print("Validation loss is", val_loss.item())
    return train_loss,val_loss


def check_accuracy(model,x_smile,x_seq,y_model,filename,device, batch_size=16, flag = 0):
    num_correct = 0
    num_samples = 0
    model.eval()
    count=1
    num_pred=[]
    num_prob=[]
    proba = []
    with torch.no_grad():
        for beg_i in range(0, x_smile.shape[0], batch_size):
            x_smile_batch = x_smile[beg_i:beg_i + batch_size]
            x_seq_batch = x_seq[beg_i:beg_i + batch_size]
            y_batch = y_model[beg_i:beg_i + batch_size]
            x_smile_batch=torch.FloatTensor(x_smile_batch)
            x_seq_batch=torch.FloatTensor(x_seq_batch)
            try:
                y_batch=y_batch.tolist()
                y_batch = y_batch.to(dtype=torch.long)
            except:
                y_batch=torch.LongTensor(list(y_batch))
            x_smile_batch = Variable(x_smile_batch)
            x_seq_batch = Variable(x_seq_batch)
            y_batch = Variable(y_batch)

            x_smile_batch=x_smile_batch.to(device)
            x_seq_batch=x_seq_batch.to(device)
            y_batch=y_batch.to(device)

            scores = model(x_smile_batch,x_seq_batch)
            _,  predictions = scores.max(1)
            
            for i in scores:
              probs = [math.exp(i[0].item()), math.exp(i[1].item())]
              #print(probs)
              proba.append(probs)
            
            probs = [i[1].item() for i in scores]
            num_pred.extend(predictions.tolist())
            num_prob.extend(probs)
            num_correct += (predictions == y_batch).sum()
            num_samples += predictions.size(0)
            count+=1
        y_model=torch.Tensor.cpu(y_model)
        accuracy=accuracy_score(np.array(y_model),np.array(num_pred))
        precision=precision_score(np.array(y_model),np.array(num_pred))
        recall=recall_score(np.array(y_model),np.array(num_pred))
        f1=f1_score(np.array(y_model),np.array(num_pred))
        roc=roc_auc_score(np.array(y_model),np.array(num_pred))
        kappa=cohen_kappa_score(np.array(y_model),np.array(num_pred))
        conf_matrix=confusion_matrix(np.array(y_model),np.array(num_pred))
        bal_acc=balanced_accuracy_score(np.array(y_model),np.array(num_pred))

        lr_fpr, lr_tpr, _ = roc_curve(np.array(y_model),np.array(num_prob))
        if(flag == 1):
            y_true = y_model
            y_probas = np.array(proba)
            skplt.metrics.plot_roc(y_true, y_probas)
            plt.savefig("{}_ROC.pdf".format(filename))
            plt.show()
            plt.close()
        else:
            plt.figure()
            plt.plot(lr_fpr, lr_tpr, marker='.', label='BLSTM (AUC = '+str(round(roc, 3))+')')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.legend()
            plt.savefig("{}_ROC.pdf".format(filename))
            plt.show()
            plt.close()
        print("Accuracy", accuracy)
        print("precision", precision)
        print("recall", recall)
        print("f1", f1)
        print("roc", roc)
        print("kappa", kappa)
        print("conf_matrix", conf_matrix)
        print("Bal_acc", bal_acc)
        return accuracy

def generate_result_matrix(model, human_smile, human_seq):
    device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu" )
    seqs=human_seq.apply(one_hot_seq)
    seqs=list(seqs)
    seqs=torch.stack(seqs).float()
    smiles = human_smile.apply(one_hot_smile)
    smiles=list(smiles)
    smiles=torch.stack(smiles).float()
    model.eval()
    pred_full_matrix = np.zeros((seqs.shape[0],smiles.shape[0]))
    prob_full_matrix = np.zeros((seqs.shape[0],smiles.shape[0]))
    for seq_index in range(len(seqs)):
        sequence = seqs[seq_index]
        sequence = sequence.view(1, sequence.shape[0],sequence.shape[1])
        for ligand_index in range(len(smiles)):
            ligand = smiles[ligand_index]
            ligand = torch.from_numpy(np.array(ligand)).float()
            ligand = ligand.view(1, ligand.shape[0],ligand.shape[1])
            #print(ligand.shape, sequence.shape)
            scores = model(ligand.to(device),sequence.to(device))
            #print(scores)
            _, predictions = scores.max(1)
            prob = torch.exp(scores)
            prob = prob.tolist()
            prob = np.max(prob[0])
            prob = float(prob)
            pred = predictions.item()
            pred_full_matrix[seq_index][ligand_index]=pred
            prob_full_matrix[seq_index][ligand_index]=prob
    return pred_full_matrix, prob_full_matrix

def convert_data(df):
    #Convert Data to suitable format for models
    X_smile_onehot = df["SMILES"].apply(one_hot_smile)
    X_seq_onehot = df["Final_Sequence"].apply(one_hot_seq)
    Y = df["Activation_Status"]
    X_smile_onehot = list(X_smile_onehot)
    X_smile_onehot = torch.stack(X_smile_onehot)
    X_seq_onehot = list(X_seq_onehot)
    X_seq_onehot = torch.stack(X_seq_onehot).float()
    Y = list(Y)
    Y = torch.Tensor(Y)
    return X_smile_onehot, X_seq_onehot, Y

def split_data(df, val_ratio = 0.15, test = False, test_ratio = 0.1):
    device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu" )
    if(test == True):
        train_df,test_df=train_test_split(df,test_size=test_ratio)
        train_df,val_df=train_test_split(train_df,test_size=val_ratio)
    else:
        train_df,val_df=train_test_split(df,test_size=val_ratio)
    #upsampling of minority data
    df_minority=train_df[train_df['Activation_Status']==1]
    df_majority=train_df[train_df['Activation_Status']==0]
    df_minority_upsampled = resample(df_minority, replace=True, n_samples=df_majority.shape[0]) 
    df_minority_upsampled = pd.concat([df_majority, df_minority_upsampled ])
    train_df=df_minority_upsampled
    train_df = train_df.sample(frac=1).reset_index(drop=True)
    print("Length of Training Data after Upsampling", len(train_df))
    print("Length of Validation Data", len(val_df))
    if(test == True):
        print("Length of Testing Data", len(test_df))
    #Conversion to pytorch format
    print("Preprocessing Data for models...")
    X_smile_onehot_train, X_seq_onehot_train, Y_train = convert_data(train_df)
    X_smile_onehot_val, X_seq_onehot_val, Y_val = convert_data(val_df)
    if(test == True):
        X_smile_onehot_test, X_seq_onehot_test, Y_test = convert_data(test_df)
        print("Preprocessing Done")
        return X_smile_onehot_train, X_seq_onehot_train, Y_train, X_smile_onehot_val, X_seq_onehot_val, Y_val, X_smile_onehot_test, X_seq_onehot_test, Y_test
    print("Preprocessing Done")
    return X_smile_onehot_train, X_seq_onehot_train, Y_train, X_smile_onehot_val, X_seq_onehot_val, Y_val

def train(X_smile_onehot_train, X_seq_onehot_train, Y_train, X_smile_onehot_val, X_seq_onehot_val, Y_val, filename="loss", learning_rate=2e-4, dropout=0.5, batch_size = 16, 
          epochs = 100, smile_h = 100, smile_l = 1, seq_h = 100, seq_l = 1):
    device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu" )
    def init_weights(m):
        if type(m) == nn.Linear:
            nn.init.xavier_normal_(m.weight)
            m.bias.data.fill_(0.01)
    model=BLSTM(77, smile_h, smile_l, 200, 27, seq_h, seq_l, 200, device, dropout = dropout, batch_size=batch_size)
    model.apply(init_weights)
    model.to(device)
    criterion= nn.NLLLoss()
    optimizer=optim.Adam(model.parameters(),lr=learning_rate)
    min_loss = 1000000
    e_losses = []
    v_losses=[]
    epochwise_train={}
    epochwise_test={}
    for e in range(epochs):
      print("epoch\t"+str(e))
      loss=train_epoch(model,X_smile_onehot_train,X_seq_onehot_train,Y_train,X_smile_onehot_val,X_seq_onehot_val,Y_val, epochwise_train,epochwise_test, e, optimizer, criterion, device, batch_size=batch_size)
      #print(loss)
      train_loss=loss[0]
      val_loss=loss[1]
      e_losses.append(train_loss.item())
      v_losses.append(val_loss.item())
    plt.plot(e_losses, label = "Train Loss")
    plt.plot(v_losses, label = "Val Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.savefig(filename+".png")
    plt.show()
    return model

def test(model, X_smile_onehot, X_seq_onehot, Y, filename, flag=0, get_acc = False):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu" )
    acc = check_accuracy(model,X_smile_onehot,X_seq_onehot,Y, filename, device, flag=flag)
    if(get_acc == True):
        return acc
    else:
        return None
    

def interpretebility(model, x_input_smile, x_input_seq, path, smile_l = 75, seq_l = 315):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu" )
    mol = Chem.MolFromSmiles(x_input_smile)
    # Chem.Kekulize(mol)
    # x_input_smile = Chem.MolToSmiles(mol, kekuleSmiles=True)
    x_user_smile = one_hot_smile(x_input_smile)
    x_user_smile = list(x_user_smile)
    x_user_smile = torch.stack(x_user_smile)
    x_user_smile = x_user_smile.view(1, smile_l, 77)

    x_user_seq = one_hot_seq(x_input_seq)
    x_user_seq = list(x_user_seq)
    x_user_seq = torch.stack(x_user_seq)
    x_user_seq = x_user_seq.view(1, seq_l, 27)
    x_user_smile.to(device)
    x_user_seq.to(device)
    model.to(device)
    model.eval()
    scores = model(x_user_smile.to(device), x_user_seq.to(device))
    #print("scores", scores)
    _, predictions = scores.max(1)
    pred_ind = predictions.item()
    prob = torch.exp(scores)
    prob = prob.tolist()
    z = [predictions.item(), float(str(prob[0][predictions.item()])[:5])]

    ig = IntegratedGradients(model)
    # baseline = torch.zeros(1, 80, 77)
    # for i in baseline[0]:
    #     i[-1]=1
    torch.backends.cudnn.enabled=False
    #print(x_user_smile.shape, x_user_seq.shape, type(x_user_smile), type(x_user_seq))
    attr, delta = ig.attribute((x_user_smile.to(device), x_user_seq.to(device)), target=1, return_convergence_delta=True)
    attr = attr[0].view(smile_l, 77)
    maxattr, _ = torch.max(attr, dim=1)
    minattr, _ = torch.min(attr, dim=1)
    relevance = maxattr + minattr
    relevance = relevance.cpu().detach().numpy()
    data_relevance = pd.DataFrame()
    data_relevance["values"] = relevance

    len_smile = min(len(x_input_smile), smile_l)

    cropped_smile_relevance = data_relevance.iloc[0:len_smile]

    x_smile_labels = pd.Series(list(x_input_smile[:len_smile]))
    cropped_smile_relevance['smile_char'] = x_smile_labels
    impacts = []

    cropped_smile_relevance['positive'] = [''] * len_smile
    cropped_smile_relevance['negative'] = [''] * len_smile
    for row in range(len_smile):
        if (ord(cropped_smile_relevance['smile_char'][row]) < 65 or ord(cropped_smile_relevance['smile_char'][row]) > 90):
            cropped_smile_relevance['values'][row] = 0
            cropped_smile_relevance['positive'][row] = 0
            cropped_smile_relevance['negative'][row] = 0
        else:
            if(cropped_smile_relevance['values'][row] > 0):
                cropped_smile_relevance['positive'][row] = cropped_smile_relevance['values'][row]
                cropped_smile_relevance['negative'][row] = 0
            elif(cropped_smile_relevance['values'][row] < 0):
                cropped_smile_relevance['negative'][row] = cropped_smile_relevance['values'][row]
                cropped_smile_relevance['positive'][row] = 0
            else:
                cropped_smile_relevance['positive'][row] = 0
                cropped_smile_relevance['negative'][row] = 0
            impacts.append(cropped_smile_relevance['values'][row])

    #print("SMILE Interpretebility")
    ax = cropped_smile_relevance.plot(y=["positive", "negative"], color=[
                                      'green', 'red'], kind="bar", figsize=(25, 15))
    ax.legend(['Contribution to Binding',
               'Contribution to Non-Binding'], prop={'size': 16})
    ax.set_xticklabels(
        cropped_smile_relevance['smile_char'], fontsize=15, rotation=0)
    ax.set_xlabel("SMILES", fontsize=15)
    ax.set_ylabel("Relevance", fontsize=15)
    ax.figure.savefig(f'{path}/SmileInterpretability.pdf')
    # ax.close()
    impacts = np.array(impacts)
    # print(impacts)

#     molecule structure interpretability
    print("Molecular Structure Interpretebility")
    mol = x_input_smile
    m = Chem.MolFromSmiles(mol)
    num_atoms = m.GetNumAtoms()
    labels = [m.GetAtomWithIdx(i).GetSymbol().upper()
              for i in range(num_atoms)]
    colors = {}
    i = 0
    k = 0
    y_max = np.max(impacts)
    y_min = np.min(impacts)
    dist = y_max - y_min
    while i < len(mol):
        c = mol[i]
        n = ""
        if c.upper() not in "CBONSPFIK":
            print(mol[i], 0.0, "0xFFFFFF")
        else:
            if i + 1 < len(mol):
                n = mol[i + 1]
            sym = c + n
            sym = sym.strip()
            com = sym.upper()
            if com == "BR" or com == "CL" or com == "NA":
                i = i + 1
            else:
                com = c.upper()
                sym = c
            if com == labels[k]:
                color = "0xBBBBBB"
                triple = [0, 0, 0]
                if impacts[k] > 0.0:
                    y = int(math.floor(255.0 - 155.0 * impacts[k] / y_max))
                    color = "0x00" + hex(y)[-2:] + "00"
                    triple[1] = y / 255.0
                if impacts[k] < 0.0:
                    y = int(math.floor(255.0 - 155.0 * impacts[k] / y_min))
                    color = "0x" + hex(y)[-2:] + "0000"
                    triple[0] = y / 255.0
                colors[k] = tuple(triple)
                print(sym, impacts[k], color)
                k = k + 1
        i = i + 1
    drawer = rdMolDraw2D.MolDraw2DSVG(400, 400)

    drawer.DrawMolecule(m, highlightAtoms=[i for i in range(
        num_atoms)], highlightBonds=[], highlightAtomColors=colors)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText().replace('svg:', '')

    fp = open(f"{path}/mol.svg", "w")
    print(svg, file=fp)
    fp.close()


#Sequence Interpretability
    #print("Sequence Interpretability")
    ax = plt.figure()
    baseline = torch.zeros(2, seq_l, 27)
    ig = IntegratedGradients(model)
    attr, delta = ig.attribute(
        (x_user_smile.to(device), x_user_seq.to(device)), target=1, return_convergence_delta=True)
    smile_attr = attr[0].view(smile_l, 77)
    seq_attr = attr[1].view(seq_l, 27)
    maxattr, _ = torch.max(seq_attr, dim=1)
    minattr, _ = torch.min(seq_attr, dim=1)
    relevance = maxattr + minattr
    relevance = relevance.cpu().detach().numpy()
    data_relevance = pd.DataFrame()
    data_relevance["values"] = relevance

    len_seq = min(len(x_input_seq), seq_l)
    cropped_seq_relevance = data_relevance.iloc[0:len_seq]

    x_seq_labels = pd.Series(list(x_input_seq[:len_seq]))
    cropped_seq_relevance['seq_char'] = x_seq_labels

    cropped_seq_relevance['positive'] = [''] * len_seq
    cropped_seq_relevance['negative'] = [''] * len_seq

    for row in range(len_seq):
        if (ord(cropped_seq_relevance['seq_char'][row]) < 65 or ord(cropped_seq_relevance['seq_char'][row]) > 90):
            cropped_seq_relevance['values'][row] = 0
            cropped_seq_relevance['positive'][row] = 0
            cropped_seq_relevance['negative'][row] = 0
        else:
            if(cropped_seq_relevance['values'][row] > 0):
                cropped_seq_relevance['positive'][row] = cropped_seq_relevance['values'][row]
                cropped_seq_relevance['negative'][row] = 0
            elif(cropped_seq_relevance['values'][row] < 0):
                cropped_seq_relevance['negative'][row] = cropped_seq_relevance['values'][row]
                cropped_seq_relevance['positive'][row] = 0
            else:
                cropped_seq_relevance['positive'][row] = 0
                cropped_seq_relevance['negative'][row] = 0

    # print(cropped_seq_relevance)

    ax = cropped_seq_relevance.plot(y=["positive", "negative"], color=[
                                    'green', 'red'], kind="barh", figsize=(20, 70))
    ax.legend(['Contribution to Binding',
               'Contribution to Non-Binding'], prop={'size': 16})
    ax.set_yticklabels(
        cropped_seq_relevance['seq_char'], fontsize=12, rotation=0)
    ax.set_ylabel("Receptor Sequence", fontsize=15)
    ax.set_xlabel("Relevance", fontsize=15, rotation=0)
    ax.figure.savefig(f'{path}/SequenceInterpretability.pdf')
    # close('all')


# In[9]:
class CPU_Unpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'torch.storage' and name == '_load_from_bytes':
            return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
        else: return super().find_class(module, name)
        
def grid_search(X_smile_onehot_train, X_seq_onehot_train, Y_train, X_smile_onehot_val, X_seq_onehot_val, Y_val, batch_size = [8, 16], learning_rate = [1e-4, 1.2e-4], dropout= [0.2, 0.5], epochs = 20):
    best_val_acc = -1
    for bs in batch_size:
        for lr in learning_rate:
            for drop in dropout:
                print("Current parameters: batch size", bs, "learning rate", lr, "dropout", drop)
                model = train(X_smile_onehot_train, X_seq_onehot_train, Y_train, X_smile_onehot_val, X_seq_onehot_val, Y_val, 
                  batch_size = bs, epochs = epochs, learning_rate=lr, dropout=drop)
                acc = test(model, X_smile_onehot_val, X_seq_onehot_val, Y_val, "val", get_acc = True)
                if(acc > best_val_acc):
                    best_val_acc = acc
                    best_bs = bs
                    best_lr = lr
                    best_drop = drop
    print("Best Parameters after grid search")
    print("Batch Size", best_bs)
    print("Learning Rate", best_lr)
    print("Best Dropout", best_drop)