from dataclasses import dataclass
import pandas as pd


@dataclass
class dpd:
    # col names of dataframe
    col_fpd0p_amt: str = "fpd0p_amt"
    col_fpd7p_amt: str = "fpd7p_amt"
    col_fpd15p_amt: str = "fpd15p_amt"
    col_fpd30p_amt: str = "fpd30p_amt"
    col_user_principal: str = "user_principal"
    col_is_fpd0: str = "is_fpd0"
    col_is_fpd7: str = "is_fpd7"
    col_is_fpd15: str = "is_fpd15"
    col_is_fpd30: str = "is_fpd30"
    col_user_cnt: str = "user_cnt"

    def dpd_basic(self, x):
        """
        Calculate fpd amount level and user level statistics from df
        expect to group by before applying the function
        example: df.groupby(['user_type']).apply(dpd_basic)
        """
        d = {}
        d['fpd0p_amt'] = (x[self.col_fpd0p_amt].sum()/x[self.col_user_principal].sum())*100
        d['fpd7p_amt'] = (x[self.col_fpd7p_amt].sum()/x[self.col_user_principal].sum())*100
        d['fpd15p_amt'] = (x[self.col_fpd15p_amt].sum()/x[self.col_user_principal].sum())*100
        d['fpd30p_amt'] = (x[self.col_fpd30p_amt].sum()/x[self.col_user_principal].sum())*100 
        d['fpd0p_user'] = (x[self.col_is_fpd0].sum()/x[self.col_user_cnt].count())*100
        d['fpd7p_user'] = (x[self.col_is_fpd7].sum()/x[self.col_user_cnt].count())*100
        d['fpd30p_user'] = (x[self.col_is_fpd30].sum()/x[self.col_user_cnt].count())*100
        d['user_cnt'] = x[self.col_user_cnt].count()
        return pd.Series(d, index=['fpd0p_amt', 'fpd7p_amt','fpd15p_amt','fpd30p_amt','fpd0p_user','fpd7p_user','fpd30p_user','user_cnt'])


