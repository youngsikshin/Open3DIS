
from open3dis.dataset.replica_loader import ReplicaReader
from open3dis.dataset.scannet_loader import ScanNetReader
from open3dis.dataset.s3dis_loader import S3DISReader


__all__ = ["ReplicaReader", "ScanNetReader", "build_dataset"]


def build_dataset(root_path, cfg):
    if cfg.data.dataset_name == "scannet200" or cfg.data.dataset_name == "scannetpp":
        return ScanNetReader(root_path, cfg)
    elif cfg.data.dataset_name == "replica":
        return ReplicaReader(root_path, cfg)
    elif cfg.data.dataset_name == "s3dis":
        return S3DISReader(root_path, cfg)
    else:
        raise ValueError(f"Unknown dataset: {cfg.data.dataset_name}")

