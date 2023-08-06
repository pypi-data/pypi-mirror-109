from typing import Tuple


class EarlyStopping:
    def __init__(self, early_stop_patience, min_delta=None, early_stop_min_delta_patience=None):
        self.inc_start_loss = 0.
        self.prev_metric_val = float("inf")
        self.inc_iter = 0
        self.min_delta_iter = 0
        self.early_stop_patience = early_stop_patience
        self.early_stop_min_delta_patience = early_stop_min_delta_patience if early_stop_min_delta_patience is not None else float(
            "inf")
        self.min_delta = min_delta if min_delta is not None else float("-inf")
        assert early_stop_patience is None or early_stop_patience >= 0
        self.increase_counting_disabled = early_stop_patience is None
        assert (early_stop_min_delta_patience is None and min_delta is None) or (
                    early_stop_min_delta_patience >= 0 and min_delta > 0)

    def __format_early_metric_name(self, metric_name):
        return "early stop metric" if metric_name is None else metric_name

    def add_metric(self, metric_val: float, metric_name=None) -> Tuple[bool, bool]:
        """[summary]

        Args:
            val_loss (float): [description]

        Returns:
            Tuple[bool, bool]: returns (should_checkpoint, should_stop)
            :param metric_name: display name of early stop metric
            :param metric_val: value of early stop metric
        """
        should_checkpoint = should_stop = False

        if not self.increase_counting_disabled and self.inc_iter > self.early_stop_patience or self.min_delta_iter > self.early_stop_min_delta_patience:
            raise ValueError("Training not stopped")

        if not self.increase_counting_disabled and metric_val > self.prev_metric_val:
            self.min_delta_iter = 0
            self.inc_iter += 1
            print('Early stop loss increased ', self.inc_iter, '/', self.early_stop_patience)
            if self.inc_iter == 1:
                print('Saving checkpoint due to increase of ', self.__format_early_metric_name(metric_name))
                should_checkpoint = True
                self.inc_start_loss = self.prev_metric_val
            if self.inc_iter > self.early_stop_patience:
                should_stop = True
                print('Stopped due to increase of ', self.__format_early_metric_name(metric_name))

        if not self.increase_counting_disabled and self.inc_iter >= 1 and metric_val <= self.inc_start_loss:
            self.inc_iter = 0
            self.inc_start_loss = 0
            print('saving checkpoint due to decrease of ', self.__format_early_metric_name(metric_name))
            should_checkpoint = True

        if metric_val <= self.prev_metric_val and self.prev_metric_val - metric_val < self.min_delta:
            self.min_delta_iter += 1
            print(self.__format_early_metric_name(metric_name), ' delta < ', self.min_delta)
            if self.min_delta_iter > self.early_stop_min_delta_patience:
                should_stop = True
                should_checkpoint = True
        else:
            self.min_delta_iter = 0

        self.prev_metric_val = metric_val
        return should_checkpoint, should_stop

    @property
    def metric_increased(self) -> bool:
        return self.inc_iter > 0
