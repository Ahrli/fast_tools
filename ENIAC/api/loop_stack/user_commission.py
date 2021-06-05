import backtrader as bt

class myCommission(bt.CommInfoBase):
    params = (
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_FIXED),

    )

    def _getcommission(self, size, price, pseudoexec):

        if size > 0:
            return self.p.rule['commission'] + (size * price * self.p.rule['stampDuty'])
        elif size < 0:
            return self.p.rule['commission']
        else:
            return 0  # just in case for some reason the size is 0.