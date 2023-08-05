from os.path import join

from .average_meter import AverageMeter
from ..tools.compat import import_optional_dependency


class NeuralNetwork(object):
    """
    A tools for a fast training process of neural network, which can start training without other code after
    the dataset, optimizer and other parameters declared.
    """

    def _raise_format_error(self, name: str, format_str: str, source_format: str):
        """
        The exception of ValueError when format was unsupported.

        :return: ValueError
        """

        raise ValueError(f"The '{ name }' should be { format_str }, rather than { source_format }")

    def __init__(self,
                 model=None,
                 train_dataset=None,
                 eval_dataset=None,
                 optimizer=None,
                 criterion=None,
                 cpu: bool = False):
        """
        Initialize the Neural Network training process.

        :param model: the torch.nn.Module
        :param train_dataset: the DataLoader() dataset for training
        :param eval_dataset: the DataLoader() dataset for testing
        :param optimizer: the torch optimizer
        :param criterion: the torch criterion
        :param cpu: set True if forced to use CPU, else it would be set automatically
        """

        # import torch for initialization
        torch = import_optional_dependency("torch")

        # ============== basic parameters ============== #
        # the device that used to train models, which can automatically set
        self.device = torch.device("cuda" if torch.cuda.is_available() and not cpu else "cpu")
        # the optimizer of training
        self.optimizer = optimizer
        # the neural network model
        self.model = model.to(self.device) if model else None
        # the criterion of training
        self.criterion = criterion.to(self.device) if criterion else None
        # the dataset for training
        self.train_dataset = train_dataset
        # the dataset for evaluation
        self.eval_dataset = eval_dataset
        # the training process would show information if self.info is True
        self.info = True

        # ============== the parameters of training ============== #
        # the loss average meter for every epoch
        self.epoch_loss = AverageMeter()
        # the counter for training
        self.epoch = 0
        # training process for iteration
        self.batch_process = None

    def _set_train(self):
        """
        A sub-function that ensuring the train mode.

        :return: None
        """

        if not self.model.__dict__['training']:
            self.model.train()

    def _set_eval(self):
        """
        A sub-function that ensuring the eval mode.

        :return: None
        """

        if self.model.__dict__['training']:
            self.model.eval()

    def _train_net(self, iter_batch: bool = False):
        """
        The train iterator that executes a standard training flow per epoch.

        :param iter_batch:
        :return:
        """

        # model initialize
        self._set_train()

        # start epoch
        for i, (source, target) in enumerate(self.train_dataset):
            # send data to device
            source = source.to(self.device)
            target = target.to(self.device)

            # the result and loss
            result = self.model(source)
            loss = self.criterion(result, target)

            # optimization and backward
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            # update the loss
            self.epoch_loss.update(loss.item(), source.size(0))

            # print the information
            if self.info:
                print(f"\rEpoch: { self.epoch } | Batch: { i } | loss: { self.epoch_loss.avg }", end="")

            # yield if iter_batch is True
            if iter_batch:
                yield result

        if self.info:
            print(f"\rEpoch: { self.epoch } | Average loss: { self.epoch_loss.avg }")

        # update epoch and reset the epoch_loss
        self.epoch_loss.reset()
        self.epoch += 1

    def _eval_net(self):
        """
        The evaluation flow using test_dataset without grad.

        :return: The total loss during evaluation and model's accuracy
        """

        # parameters initialize
        torch = import_optional_dependency("torch")
        eval_total = 0
        eval_correct = 0
        eval_loss = 0
        self._set_eval()

        # display the information
        if self.info:
            print(f"\rEvaluating...", end="")

        # start eval part
        for i, (source, target) in enumerate(self.eval_dataset):
            # send data to device
            source = source.to(self.device)
            target = target.to(self.device)

            result = self.model(source)
            eval_loss += self.criterion(result, target).item()
            _, predicted = torch.max(result.data, 1)
            eval_total += target.size(0)
            eval_correct += (predicted == target).sum().item()

        accuracy = eval_correct / eval_total
        eval_loss = eval_loss / eval_total

        if self.info:
            print(f"\rEvaluation loss: { eval_loss } | Accuracy: { accuracy }")

        return eval_loss, accuracy

    @staticmethod
    def _reset_weight(m):
        """
        A sub-function with a general weights initialization.

        :param m: the layers of self.model
        :return: None
        """

        nn = import_optional_dependency("torch.nn")
        init = import_optional_dependency("torch.nn.init")
        if isinstance(m, nn.Conv1d):
            init.normal_(m.weight.data)
            if m.bias is not None:
                init.normal_(m.bias.data)
        elif isinstance(m, nn.Conv2d):
            init.xavier_normal_(m.weight.data)
            if m.bias is not None:
                init.normal_(m.bias.data)
        elif isinstance(m, nn.Conv3d):
            init.xavier_normal_(m.weight.data)
            if m.bias is not None:
                init.normal_(m.bias.data)
        elif isinstance(m, nn.ConvTranspose1d):
            init.normal_(m.weight.data)
            if m.bias is not None:
                init.normal_(m.bias.data)
        elif isinstance(m, nn.ConvTranspose2d):
            init.xavier_normal_(m.weight.data)
            if m.bias is not None:
                init.normal_(m.bias.data)
        elif isinstance(m, nn.ConvTranspose3d):
            init.xavier_normal_(m.weight.data)
            if m.bias is not None:
                init.normal_(m.bias.data)
        elif isinstance(m, nn.BatchNorm1d):
            init.normal_(m.weight.data, mean=1, std=0.02)
            init.constant_(m.bias.data, 0)
        elif isinstance(m, nn.BatchNorm2d):
            init.normal_(m.weight.data, mean=1, std=0.02)
            init.constant_(m.bias.data, 0)
        elif isinstance(m, nn.BatchNorm3d):
            init.normal_(m.weight.data, mean=1, std=0.02)
            init.constant_(m.bias.data, 0)
        elif isinstance(m, nn.Linear):
            init.xavier_normal_(m.weight.data)
            init.normal_(m.bias.data)
        elif isinstance(m, nn.LSTM):
            for param in m.parameters():
                if len(param.shape) >= 2:
                    init.orthogonal_(param.data)
                else:
                    init.normal_(param.data)
        elif isinstance(m, nn.LSTMCell):
            for param in m.parameters():
                if len(param.shape) >= 2:
                    init.orthogonal_(param.data)
                else:
                    init.normal_(param.data)
        elif isinstance(m, nn.GRU):
            for param in m.parameters():
                if len(param.shape) >= 2:
                    init.orthogonal_(param.data)
                else:
                    init.normal_(param.data)
        elif isinstance(m, nn.GRUCell):
            for param in m.parameters():
                if len(param.shape) >= 2:
                    init.orthogonal_(param.data)
                else:
                    init.normal_(param.data)

    def __repr__(self):
        """
        Show the information of training.

        :return: None
        """

        # info string
        info = self.model.__repr__()
        info += "\n=========================\n"
        info += f"Train data length:\t\t{ len(self.train_dataset) }\n"
        info += f"Eval sata length:\t\t{ len(self.eval_dataset) }\n"
        info += f"Optimizer:\t\t\t\t{ str(self.optimizer).split('(')[0] }\n"
        info += f"Criterion:\t\t\t\t{ str(self.criterion).split('(')[0] }\n"
        info += f"Training Environment:\t{ self.device.type }\n"
        info += f"Show information:\t\t{ 'True' if self.info else 'False' }\n"
        info += "=========================\n"

        return info

    def auto_train(self,
                   epoch: int,
                   save_model_location: str,
                   eval: bool = True,
                   eval_interval: int = 1,
                   info: bool = True,
                   save_static_dicts: bool = True):
        """
        A auto training method for fast using. And the epoch and the location for saving models should be
        specified while using auto_train().

        :param epoch: teh epoch of training
        :param save_model_location: the location for storing the model
        :param eval: eval the model or not
        :param eval_interval: the interval epoch between each eval processes
        :param info: Show the information or not
        :param save_static_dicts: set True if only save the static dicts
        :return: None
        """

        # initialize
        self.info = info
        best_attempt = float("-inf")
        self._set_train()

        # start training
        for n in range(epoch):
            self._train_net()
            if self.eval_dataset and eval and not (n + 1) % eval_interval:
                # eval start
                eval_loss, accuracy = self._eval_net()

                # save the best model
                if accuracy > best_attempt:
                    best_attempt = accuracy
                    if save_static_dicts:
                        self.save_state_dict(join(save_model_location, 'model.pkl'))
                    else:
                        self.save_model(join(save_model_location, 'model.pkl'))

    def iter_epoch(self):
        """
        An iterator that training per epoch and return for advanced calculation, plot, etc.

        :return: None
        """

        # set to train mode
        self._set_train()
        self._train_net()

    def iter_batch(self):
        """
        An iterator that training per batch and return for advanced calculation, plot, etc.

        :return: output
        """

        if not self.batch_process:
            self.batch_process = self._train_net(iter_batch=True)
            return self.batch_process.__next__()
        else:
            return self.batch_process.__next__()

    def eval(self):
        """
        The evaluation function.

        :return: None
        """

        self._eval_net()

    def reset_train(self):
        """
        Reset the process of training, which includes the loss meter reset, epoch reset and model's weights
        reset.

        :return: None
        """

        self.model.apply(self._reset_weight)
        self.epoch_loss.reset()
        self.epoch = 0
        self.batch_process = None

    def save_state_dict(self, location: str):
        """
        Save only the state dict of the model.

        :param location: the location of models
        :return: None
        """

        torch = import_optional_dependency("torch")
        torch.save(self.model.state_dict(), location)

    def save_model(self, location: str):
        """
        Save only the whole model.

        :param location: the location of models
        :return: None
        """

        torch = import_optional_dependency("torch")
        torch.save(self.model, location)

    def check_parameters(self):
        """
        A method for checking the parameters before training, in order to process the training correctly.

        :return: None
        """

        torch = import_optional_dependency('torch')
        if not isinstance(self.model, torch.nn.Module):
            self._raise_format_error('self.model', 'torch.nn.Module', f'{ type(self.model) }')
        if not isinstance(self.optimizer, torch.optim.Optimizer):
            self._raise_format_error('self.optimizer', 'torch.optim.Optimizer', f'{ type(self.optimizer) }')
        if not isinstance(self.train_dataset, torch.utils.data.DataLoader):
            self._raise_format_error('self.train_dataset', 'torch.utils.data.DataLoader', f'{ type(self.train_dataset) }')
        if not isinstance(self.eval_dataset, torch.utils.data.DataLoader):
            self._raise_format_error('self.eval_dataset', 'torch.utils.data.DataLoader', f'{ type(self.eval_dataset) }')
