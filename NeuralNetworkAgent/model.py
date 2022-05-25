import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import shutil

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x)).cuda() 
        x = self.linear2(x).cuda() 
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)
        # here we can save the model to another format
        #model_scripted = torch.jit.script(self) # Export to TorchScript
        #model_scripted.save('./model/model_scripted.pt') # Save

    def save_ckp(self, state, is_best, checkpoint_dir, best_model_dir):
        f_path = './checkpoint/checkpoint.pt'
        torch.save(state, f_path)
        if is_best:
            best_fpath = './model/best_model.pt'
            shutil.copyfile(f_path, best_fpath)

    def load_ckp(checkpoint_fpath, model, optimizer):
        checkpoint = torch.load('./checkpoint/checkpoint.pt')
        model.load_state_dict(checkpoint['state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        return model, optimizer, checkpoint['epoch']


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model.cuda() 
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

        # here we (TRY) get it to resume from a previous model
        # only do this if the file exists
        if os.path.exists("./checkpoint/checkpoint.pt"):
            model = model.cuda()
            optimizer = optim.Adam(model.parameters(), lr=self.lr)
            ckp_path = "./checkpoint/checkpoint.pt"
            self.model, self.optimizer, start_epoch = Linear_QNet.load_ckp(ckp_path, model, optimizer)

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float).cuda() 
        next_state = torch.tensor(next_state, dtype=torch.float).cuda() 
        action = torch.tensor(action, dtype=torch.float).cuda() 
        reward = torch.tensor(reward, dtype=torch.float).cuda() 
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx])).cuda() 

            
            target[idx][torch.argmax(action).item()] = Q_new ## to understand what this is, check "Teahc AI To Play Snake - Reinforncement Learning tutorial" @ 21:38

        # 2: Q_new =  + y * max(newx_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()

