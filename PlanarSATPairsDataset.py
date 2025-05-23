import torch
from torch_geometric.data import InMemoryDataset
from torch.serialization import add_safe_globals,safe_globals
import pickle
import os
from torch_geometric.utils import to_networkx
NAME = "GRAPHSAT"
from torch.serialization import add_safe_globals
from torch_geometric.data import Data, HeteroData
from torch_geometric.data.data import DataEdgeAttr



class PlanarSATPairsDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None, pre_filter=None):
        super(PlanarSATPairsDataset, self).__init__(root, transform, pre_transform, pre_filter)
        print(DataEdgeAttr.__module__, DataEdgeAttr.__name__)
        with safe_globals({("torch_geometric.data.data", "DataEdgeAttr"): DataEdgeAttr}):
            self.data, self.slices = torch.load(self.processed_paths[0],weights_only=False)
    @property
    def raw_file_names(self):
        return [NAME+".pkl"]

    @property
    def processed_file_names(self):
        return 'data.pt'

    def download(self):
        pass  

    def process(self):
        # Read data into huge `Data` list.
        print(os.getcwd())
        data_list = pickle.load(open(os.path.join(self.root, "raw/"+NAME+".pkl"), "rb"))

        if self.pre_filter is not None:
            data_list = [data for data in data_list if self.pre_filter(data)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])


if __name__ == "__main__":
    test_path = "Data/EXP/"
    dataset = PlanarSATPairsDataset(test_path)
    print(dataset[0])
