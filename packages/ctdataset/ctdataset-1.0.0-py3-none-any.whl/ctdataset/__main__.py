if __name__ == "__main__":
    import argparse
    from ctdataset.dataset import CTDataset
    from torch.utils.data import DataLoader
    from tqdm import tqdm
    from ctnet import CTNet
    from torch.optim import Adam
    from torch.nn import BCELoss
    parser = argparse.ArgumentParser(description='Process some integers.')
    ########################################### LOADER RELATED #########################################################
    parser.add_argument('ply_folder')
    ################################################ HP ################################################################
    parser.add_argument('--dim', default=96, type=int, help="64,96")
    parser.add_argument('--bs', default=10, type=int, help="100,30")
    parser.add_argument('--strech_box', action="store_true")
    parser.add_argument('--no_shuffle', action="store_true")
    parser.add_argument('--dense', action="store_true")
    parser.add_argument('--lr', default=pow(10, -3), type=float)
    parser.add_argument('--num_workers', default=1, type=int)
    parser.add_argument('--t', default=0.9, type=float)
    parser.add_argument('--device', default="cuda", type=str)

    args = parser.parse_args()

    # Model
    model = CTNet(args.dim, id=f"ctnet{args.dim}{'_dense_' if args.dense else '_'}streched_{args.strech_box}").cuda()
    # Loader
    dataset = CTDataset(ply_folder=args.ply_folder, dim=args.dim)
    # Model variables
    loader = DataLoader(dataset=dataset,
                        batch_size=args.bs,
                        num_workers=args.num_workers,
                        shuffle=not args.no_shuffle,
                        persistent_workers=True,
                        pin_memory=True,
                        drop_last=True)

    # self.train_loader.dataset.shuffle() if self.shuffle else None
    optimizer=Adam(model.parameters(), lr=pow(10, -4))
    model.train()
    criterion = BCELoss()
    for epoch in range(10):
        for i, (x, y, _, _, _) in tqdm(enumerate(loader), total=len(loader), desc=f">> Epoch {epoch}"):
            x = x.cuda()
            y = y.cuda()

            optimizer.zero_grad()
            x, y = x.cuda(), y.cuda()
            _y = model(x)
            loss = criterion(_y, y)
            loss = loss / _y.size(1)  # average the loss by minibatch
            loss.backward()

