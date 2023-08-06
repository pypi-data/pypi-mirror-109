# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 17:47:01 2021

Who would be so cruel to someone like you?
No one but you
Who would make the rules for the things that you do?
No one but you
I woke up this morning, looked at the sky
I thought of all of the time passing by
It didn't matter how hard we tried
'Cause in the end

@author: KING
"""

from sympy import symbols, solve
from sklearn.neural_network import MLPRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import statsmodels.discrete.discrete_model as logitm
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns
import statsmodels.regression.linear_model as lm_
import statsmodels.robust.robust_linear_model as roblm_
import statsmodels.regression.quantile_regression as QREG
from scipy import stats

eEdata =  pd.read_excel(r'C:\Users\KING\Desktop\复现\Triumphant.xlsx')


def log_series(x):## log10 以10为底数
    ou = []
    for ir in range(0,len(x)):
        try:
            xs = math.log(x[ir],10)
            ou.append(xs)
        except:
            xs = np.nan
            ou.append(xs)
    oui = pd.Series(ou)
    return oui 

def pvaluestr(sa_1):
    if sa_1 <= 0.001:
        res = 'p < 0.001'     
    if sa_1 > 0.001:
        res = 'p  = '+ str(np.round(sa_1,4))
    return res

def TUQ(forV,forx,const,lake,Double):
    if lake == True:
        eEdatatype = eEdata[eEdata['Type']!='reservoirs']
        eEdata_fR1  = eEdatatype
        blp = pd.concat([eEdata_fR1[forV],eEdata_fR1[forx]],axis=1)
        ch4Y = blp.dropna(axis=0).reset_index(drop=True)
        CH4_yfor = log_series(ch4Y[forV] + const )
        ch4_chla = log_series(ch4Y[forx])
        u = CH4_yfor.mean()  
        std = CH4_yfor.std()  
        stats.kstest(CH4_yfor, 'norm', (u, std))
        error = CH4_yfor[np.abs(CH4_yfor - u) > 3*std]
        data_c = CH4_yfor[np.abs(CH4_yfor - u) <= 3*std]
        CH4_chla_TT = ch4_chla.drop(index=error.index)
        CH4_yfor_TT = CH4_yfor.drop(index=error.index)
        CH4_chla_TT = CH4_chla_TT.dropna()
        CH4_yfor_TT = CH4_yfor_TT.dropna()
        ch4merge = pd.concat([CH4_chla_TT,CH4_yfor_TT],axis=1)
        ch4merge3 = ch4merge.dropna()
        CH4_chla_TT = ch4merge3.iloc[:,0].reset_index(drop=True)
        CH4_yfor_TT = ch4merge3.iloc[:,1].reset_index(drop=True)
        return CH4_yfor_TT,CH4_chla_TT
        if Double == True :
            u_d = CH4_chla_TT.mean()  
            std_d = CH4_yfor_TT.std() 
            stats.kstest(CH4_chla_TT, 'norm', (u_d, std_d))
            error_d = CH4_chla_TT[np.abs(CH4_chla_TT - u_d) > 3*std_d]
            data_d = CH4_chla_TT[np.abs(CH4_chla_TT - u_d) <= 3*std_d]
            CH4_chla_TT2 = CH4_chla_TT.drop(index=error.index).reset_index(drop=True)
            CH4_yfor_TT2 = CH4_yfor_TT.drop(index=error.index).reset_index(drop=True)
            return CH4_yfor_TT2,CH4_chla_TT2
    
    if lake == False:
        eEdatatype = eEdata[eEdata['Type']=='reservoirs']
        eEdata_fR1  = eEdatatype
        blp = pd.concat([eEdata_fR1[forV],eEdata_fR1[forx]],axis=1)
        ch4Y = blp.dropna(axis=0).reset_index(drop=True)
        CH4_yfor = log_series(ch4Y[forV] + const )
        ch4_chla = log_series(ch4Y[forx])
        u = CH4_yfor.mean()  
        std = CH4_yfor.std()  
        stats.kstest(CH4_yfor, 'norm', (u, std))
        error = CH4_yfor[np.abs(CH4_yfor - u) > 3*std]
        data_c = CH4_yfor[np.abs(CH4_yfor - u) <= 3*std]
        CH4_chla_TT = ch4_chla.drop(index=error.index)
        CH4_yfor_TT = CH4_yfor.drop(index=error.index)
        CH4_chla_TT = CH4_chla_TT.dropna()
        CH4_yfor_TT = CH4_yfor_TT.dropna()
        ch4merge = pd.concat([CH4_chla_TT,CH4_yfor_TT],axis=1)
        ch4merge3 = ch4merge.dropna()
        CH4_chla_TT = ch4merge3.iloc[:,0].reset_index(drop=True)
        CH4_yfor_TT = ch4merge3.iloc[:,1].reset_index(drop=True)
        return CH4_yfor_TT,CH4_chla_TT
        if Double == True :
            u_d = CH4_chla_TT.mean()  
            std_d = CH4_yfor_TT.std() 
            stats.kstest(CH4_chla_TT, 'norm', (u_d, std_d))
            error_d = CH4_chla_TT[np.abs(CH4_chla_TT - u_d) > 3*std_d]
            data_d = CH4_chla_TT[np.abs(CH4_chla_TT - u_d) <= 3*std_d]
            CH4_chla_TT2 = CH4_chla_TT.drop(index=error.index).reset_index(drop=True)
            CH4_yfor_TT2 = CH4_yfor_TT.drop(index=error.index).reset_index(drop=True)
            return CH4_yfor_TT2,CH4_chla_TT2





def KD(CH4_yfor_TT,CH4_chla_TT,Yname,Xname):
    dataX = sm.add_constant(CH4_chla_TT)
    ols_result = sm.OLS(CH4_yfor_TT, dataX).fit()     
    rlm_result = sm.RLM(CH4_yfor_TT, dataX).fit() 
    mid_result = QREG.QuantReg(CH4_yfor_TT, dataX).fit(q=0.5) 
    ols_p = np.round(ols_result.pvalues.iloc[1],9)
    ols_para = np.round(ols_result.params.iloc[1],3)
    rlm_p = np.round(rlm_result.pvalues.iloc[1],9)
    rlm_para = np.round(rlm_result.params.iloc[1],3)
    mid_p = np.round(mid_result.pvalues.iloc[1],9)
    mid_para = np.round(mid_result.params.iloc[1],3)
    p_COLI = [ols_p,rlm_p, mid_p]
    if ols_p == np.min(p_COLI):
        final_p = ols_p
        final_para = ols_para
    if rlm_p == np.min(p_COLI):
        final_p = rlm_p
        final_para = rlm_para
    if mid_p == np.min(p_COLI):
        final_p = mid_p
        final_para = mid_para
    return final_p,final_para


def POLTall(forx,Xname):
    if forx != 'chla_execute':
        font_Yble = {'family': 'serif','style': 'italic','weight': 'normal','color':  'black', 'size': 8,};   
        font_Ylae = {'family': 'serif','style': 'italic','weight': 'normal','color':  'black', 'size': 10,};   
        ax1Y = TUQ('ch4_t',forx,0,True,False)[0]
        ax1X = TUQ('ch4_t',forx,0,True,False)[1]
        ax1_p = KD(ax1Y,ax1X,'Total CH4',Xname)[0]
        ax1_param = KD(ax1Y,ax1X,'Total CH4',Xname)[1]
        ax2Y = TUQ('co2',forx,328.22,True,False)[0]
        ax2X = TUQ('co2',forx,328.22,True,False)[1]
        ax2_p = KD(ax2Y,ax2X,'CO2',Xname)[0]
        ax2_param = KD(ax2Y,ax2X,'CO2',Xname)[1]
        ax3Y = TUQ('n2o',forx,0.1,True,False)[0]
        ax3X = TUQ('n2o',forx,0.1,True,False)[1]
        ax3_p = KD(ax3Y,ax3X,'N2O',Xname)[0]
        ax3_param = KD(ax3Y,ax3X,'N2O',Xname)[1]
        ax4Y = TUQ('chla_execute',forx,0,True,False)[0]
        ax4X = TUQ('chla_execute',forx,0,True,False)[1]
        ax4_p = KD(ax4Y,ax4X,'chla',Xname)[0]
        ax4_param = KD(ax4Y,ax4X,'chla',Xname)[1]
        ax5Y = TUQ('ch4_t',forx,1.5,False,False)[0]
        ax5X = TUQ('ch4_t',forx,1.5,False,False)[1]
        ax5_p = KD(ax5Y,ax5X,'Total CH4',Xname)[0]
        ax5_param = KD(ax5Y,ax5X,'Total CH4',Xname)[1]
        ax6Y = TUQ('co2',forx,1030.045,False,False)[0]
        ax6X = TUQ('co2',forx,1030.045,False,False)[1]
        ax6_p = KD(ax6Y,ax6X,'CO2',Xname)[0]
        ax6_param = KD(ax6Y,ax6X,'CO2',Xname)[1]
        ax7Y = TUQ('n2o',forx,0.12,False,False)[0]
        ax7X = TUQ('n2o',forx,0.12,False,False)[1]
        ax7_p = KD(ax7Y,ax7X,'N2O',Xname)[0]
        ax7_param = KD(ax7Y,ax7X,'N2O',Xname)[1]
        ax8Y = TUQ('chla_execute',forx,0,False,False)[0]
        ax8X = TUQ('chla_execute',forx,0,False,False)[1]
        ax8_p = KD(ax8Y,ax8X,'chla',Xname)[0]
        ax8_param = KD(ax8Y,ax8X,'chla',Xname)[1]
        fig=plt.figure(figsize=(12,5),dpi=300)
        ax1=fig.add_subplot(241) 
        ax1.scatter(ax1X,ax1Y,s=50,c='#336666',alpha=0.5,marker='.')
        sns.regplot(ax1X,ax1Y,ax=ax1,scatter=False,ci=0,color = '#336666')
        mark1 = pvaluestr(float(ax1_p)) + '| Slope {'+str(np.round(float(ax1_param),2))+ '}'
        ax1.annotate( mark1  ,xy=(np.quantile(ax1X,0.08),np.quantile(ax1Y,0.3)),xytext=(np.min(ax1X)+0.1,np.quantile(ax1Y,0.8)))
        ax1.set_title('Lake| Net effect of ' + Xname + ' on Total CH4'    ,fontdict=font_Ylae)
        ax1.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax1.set_ylabel('Total CH4 flux mg_CH4-C_m_2_d_1(logarithm)',fontdict=font_Yble)
        ax2=fig.add_subplot(242) 
        ax2.scatter(ax2X,ax2Y,s=50,c='#669999',alpha=0.5,marker='.')
        sns.regplot(ax2X,ax2Y,ax=ax2,scatter=False,ci=0,color = '#669999')
        mark2 = pvaluestr(float(ax2_p)) + '| Slope {'+str(np.round(float(ax2_param),2))+ '}'
        ax2.annotate( mark2  ,xy=(np.quantile(ax2X,0.08),np.quantile(ax2Y,0.3)),xytext=(np.min(ax2X)+0.1,np.quantile(ax2Y,0.8)))
        ax2.set_title('Lake| Net effect of ' + Xname + ' on CO2'    ,fontdict=font_Ylae)
        ax2.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax2.set_ylabel('CO2 flux mg_CO2-C_m_2_d_1(logarithm)',fontdict=font_Yble)
        ax3=fig.add_subplot(243) 
        ax3.scatter(ax3X,ax3Y,s=50,c='#339999',alpha=0.5,marker='.')
        sns.regplot(ax3X,ax3Y,ax=ax3,scatter=False,ci=0,color = '#339999')
        mark3 = pvaluestr(float(ax3_p)) + '| Slope {'+str(np.round(float(ax3_param),2))+ '}'
        ax3.annotate( mark3  ,xy=(np.quantile(ax3X,0.08),np.quantile(ax3Y,0.3)),xytext=(np.min(ax3X)+0.1,np.quantile(ax3Y,0.8)))
        ax3.set_title('Lake| Net effect of ' + Xname + ' on N2O'    ,fontdict=font_Ylae)
        ax3.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax3.set_ylabel('N2O flux mg_N2O-N_m_2_d_1(logarithm)',fontdict=font_Yble)
        ax4=fig.add_subplot(244) 
        ax4.scatter(ax4X,ax4Y,s=50,c='#336699',alpha=0.5,marker='.')
        sns.regplot(ax4X,ax4Y,ax=ax4,scatter=False,ci=0,color = '#336699')
        mark4 = pvaluestr(float(ax4_p)) + '| Slope {'+str(np.round(float(ax4_param),2))+ '}'
        ax4.annotate( mark4  ,xy=(np.quantile(ax4X,0.08),np.quantile(ax4Y,0.3)),xytext=(np.min(ax4X)+0.1,np.quantile(ax4Y,0.8)))
        ax4.set_title('Lake| Net effect of ' + Xname + ' on chla'    ,fontdict=font_Ylae)
        ax4.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax4.set_ylabel('chla (logarithm)',fontdict=font_Yble)
        ax5=fig.add_subplot(245) 
        ax5.scatter(ax5X,ax5Y,s=50,c='#336666',alpha=0.5,marker='.')
        sns.regplot(ax5X,ax5Y,ax=ax5,scatter=False,ci=0,color = '#336666')
        mark5 = pvaluestr(float(ax5_p)) + '| Slope {'+str(np.round(float(ax5_param),2))+ '}'
        ax5.annotate( mark5  ,xy=(np.quantile(ax5X,0.08),np.quantile(ax5Y,0.3)),xytext=(np.min(ax5X)+0.1,np.quantile(ax5Y,0.8)))
        ax5.set_title('Reservoir| Net effect of ' + Xname + ' on Total CH4'    ,fontdict=font_Ylae)
        ax5.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax5.set_ylabel('',fontdict=font_Yble)
        ax6=fig.add_subplot(246) 
        ax6.scatter(ax6X,ax6Y,s=50,c='#669999',alpha=0.5,marker='.')
        sns.regplot(ax6X,ax6Y,ax=ax6,scatter=False,ci=0,color = '#669999')
        mark6 = pvaluestr(float(ax6_p)) + '| Slope {'+str(np.round(float(ax6_param),2))+ '}'
        ax6.annotate( mark6  ,xy=(np.quantile(ax6X,0.08),np.quantile(ax6Y,0.3)),xytext=(np.min(ax6X)+0.1,np.quantile(ax6Y,0.8)))
        ax6.set_title('Reservoir| Net effect of ' + Xname + ' on CO2'    ,fontdict=font_Ylae)
        ax6.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax6.set_ylabel('',fontdict=font_Yble)
        ax7=fig.add_subplot(247) 
        ax7.scatter(ax7X,ax7Y,s=50,c='#339999',alpha=0.5,marker='.')
        sns.regplot(ax7X,ax7Y,ax=ax7,scatter=False,ci=0,color = '#339999')
        mark7 = pvaluestr(float(ax7_p)) + '| Slope {'+str(np.round(float(ax7_param),2))+ '}'
        ax7.annotate( mark7  ,xy=(np.quantile(ax7X,0.08),np.quantile(ax7Y,0.3)),xytext=(np.min(ax7X)+0.1,np.quantile(ax7Y,0.8)))
        ax7.set_title('Reservoir| Net effect of ' + Xname + ' on N2O'    ,fontdict=font_Ylae)
        ax7.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax7.set_ylabel('',fontdict=font_Yble)
        ax8=fig.add_subplot(248) 
        ax8.scatter(ax8X,ax8Y,s=50,c='#336699',alpha=0.5,marker='.')
        sns.regplot(ax8X,ax8Y,ax=ax8,scatter=False,ci=0,color = '#336699')
        mark8 = pvaluestr(float(ax8_p)) + '| Slope {'+str(np.round(float(ax8_param),2))+ '}'
        ax8.annotate( mark8  ,xy=(np.quantile(ax8X,0.08),np.quantile(ax8Y,0.3)),xytext=(np.min(ax8X)+0.1,np.quantile(ax8Y,0.8)))
        ax8.set_title('Reservoir| Net effect of ' + Xname + ' on chla'    ,fontdict=font_Ylae)
        ax8.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax8.set_ylabel('',fontdict=font_Yble)
        plt.tight_layout()
    if forx == 'chla_execute':    
        font_Yble = {'family': 'serif','style': 'italic','weight': 'normal','color':  'black', 'size': 8,};   
        font_Ylae = {'family': 'serif','style': 'italic','weight': 'normal','color':  'black', 'size': 10,};   
        ax1Y = TUQ('ch4_t',forx,0,True,False)[0]
        ax1X = TUQ('ch4_t',forx,0,True,False)[1]
        ax1_p = KD(ax1Y,ax1X,'Total CH4',Xname)[0]
        ax1_param = KD(ax1Y,ax1X,'Total CH4',Xname)[1]
        ax2Y = TUQ('co2',forx,328.22,True,False)[0]
        ax2X = TUQ('co2',forx,328.22,True,False)[1]
        ax2_p = KD(ax2Y,ax2X,'CO2',Xname)[0]
        ax2_param = KD(ax2Y,ax2X,'CO2',Xname)[1]
        ax3Y = TUQ('n2o',forx,0.1,True,False)[0]
        ax3X = TUQ('n2o',forx,0.1,True,False)[1]
        ax3_p = KD(ax3Y,ax3X,'N2O',Xname)[0]
        ax3_param = KD(ax3Y,ax3X,'N2O',Xname)[1]
        ax5Y = TUQ('ch4_t',forx,1.5,False,False)[0]
        ax5X = TUQ('ch4_t',forx,1.5,False,False)[1]
        ax5_p = KD(ax5Y,ax5X,'Total CH4',Xname)[0]
        ax5_param = KD(ax5Y,ax5X,'Total CH4',Xname)[1]
        ax6Y = TUQ('co2',forx,1030.045,False,False)[0]
        ax6X = TUQ('co2',forx,1030.045,False,False)[1]
        ax6_p = KD(ax6Y,ax6X,'CO2',Xname)[0]
        ax6_param = KD(ax6Y,ax6X,'CO2',Xname)[1]
        ax7Y = TUQ('n2o',forx,0.12,False,False)[0]
        ax7X = TUQ('n2o',forx,0.12,False,False)[1]
        ax7_p = KD(ax7Y,ax7X,'N2O',Xname)[0]
        ax7_param = KD(ax7Y,ax7X,'N2O',Xname)[1]
     
        fig=plt.figure(figsize=(12,5),dpi=300)
        ax1=fig.add_subplot(231) 
        ax1.scatter(ax1X,ax1Y,s=50,c='#336666',alpha=0.5,marker='.')
        sns.regplot(ax1X,ax1Y,ax=ax1,scatter=False,ci=0,color = '#336666')
        mark1 = pvaluestr(float(ax1_p)) + '| Slope {'+str(np.round(float(ax1_param),2))+ '}'
        ax1.annotate( mark1  ,xy=(np.quantile(ax1X,0.08),np.quantile(ax1Y,0.3)),xytext=(np.min(ax1X)+0.1,np.quantile(ax1Y,0.8)))
        ax1.set_title('Lake| Net effect of ' + Xname + ' on Total CH4'    ,fontdict=font_Ylae)
        ax1.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax1.set_ylabel('Total CH4 flux mg_CH4-C_m_2_d_1(logarithm)',fontdict=font_Yble)
        ax2=fig.add_subplot(232) 
        ax2.scatter(ax2X,ax2Y,s=50,c='#669999',alpha=0.5,marker='.')
        sns.regplot(ax2X,ax2Y,ax=ax2,scatter=False,ci=0,color = '#669999')
        mark2 = pvaluestr(float(ax2_p)) + '| Slope {'+str(np.round(float(ax2_param),2))+ '}'
        ax2.annotate( mark2  ,xy=(np.quantile(ax2X,0.08),np.quantile(ax2Y,0.3)),xytext=(np.min(ax2X)+0.1,np.quantile(ax2Y,0.8)))
        ax2.set_title('Lake| Net effect of ' + Xname + ' on CO2'    ,fontdict=font_Ylae)
        ax2.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax2.set_ylabel('CO2 flux mg_CO2-C_m_2_d_1(logarithm)',fontdict=font_Yble)
        ax3=fig.add_subplot(233) 
        ax3.scatter(ax3X,ax3Y,s=50,c='#339999',alpha=0.5,marker='.')
        sns.regplot(ax3X,ax3Y,ax=ax3,scatter=False,ci=0,color = '#339999')
        mark3 = pvaluestr(float(ax3_p)) + '| Slope {'+str(np.round(float(ax3_param),2))+ '}'
        ax3.annotate( mark3  ,xy=(np.quantile(ax3X,0.08),np.quantile(ax3Y,0.3)),xytext=(np.min(ax3X)+0.1,np.quantile(ax3Y,0.8)))
        ax3.set_title('Lake| Net effect of ' + Xname + ' on N2O'    ,fontdict=font_Ylae)
        ax3.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax3.set_ylabel('N2O flux mg_N2O-N_m_2_d_1(logarithm)',fontdict=font_Yble)
      
        ax5=fig.add_subplot(234) 
        ax5.scatter(ax5X,ax5Y,s=50,c='#336666',alpha=0.5,marker='.')
        sns.regplot(ax5X,ax5Y,ax=ax5,scatter=False,ci=0,color = '#336666')
        mark5 = pvaluestr(float(ax5_p)) + '| Slope {'+str(np.round(float(ax5_param),2))+ '}'
        ax5.annotate( mark5  ,xy=(np.quantile(ax5X,0.08),np.quantile(ax5Y,0.3)),xytext=(np.min(ax5X)+0.1,np.quantile(ax5Y,0.8)))
        ax5.set_title('Reservoir| Net effect of ' + Xname + ' on Total CH4'    ,fontdict=font_Ylae)
        ax5.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax5.set_ylabel('',fontdict=font_Yble)
        ax6=fig.add_subplot(235) 
        ax6.scatter(ax6X,ax6Y,s=50,c='#669999',alpha=0.5,marker='.')
        sns.regplot(ax6X,ax6Y,ax=ax6,scatter=False,ci=0,color = '#669999')
        mark6 = pvaluestr(float(ax6_p)) + '| Slope {'+str(np.round(float(ax6_param),2))+ '}'
        ax6.annotate( mark6  ,xy=(np.quantile(ax6X,0.08),np.quantile(ax6Y,0.3)),xytext=(np.min(ax6X)+0.1,np.quantile(ax6Y,0.8)))
        ax6.set_title('Reservoir| Net effect of ' + Xname + ' on CO2'    ,fontdict=font_Ylae)
        ax6.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax6.set_ylabel('',fontdict=font_Yble)
        ax7=fig.add_subplot(236) 
        ax7.scatter(ax7X,ax7Y,s=50,c='#339999',alpha=0.5,marker='.')
        sns.regplot(ax7X,ax7Y,ax=ax7,scatter=False,ci=0,color = '#339999')
        mark7 = pvaluestr(float(ax7_p)) + '| Slope {'+str(np.round(float(ax7_param),2))+ '}'
        ax7.annotate( mark7  ,xy=(np.quantile(ax7X,0.08),np.quantile(ax7Y,0.3)),xytext=(np.min(ax7X)+0.1,np.quantile(ax7Y,0.8)))
        ax7.set_title('Reservoir| Net effect of ' + Xname + ' on N2O'    ,fontdict=font_Ylae)
        ax7.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
        ax7.set_ylabel('',fontdict=font_Yble)
        plt.tight_layout()        
    return 


#%% 甲烷扩散通量和蒸腾通量

def POLTall_ch4E(forx,Xname):
    font_Yble = {'family': 'serif','style': 'italic','weight': 'normal','color':  'black', 'size': 8,};   
    font_Ylae = {'family': 'serif','style': 'italic','weight': 'normal','color':  'black', 'size': 10,};   
    ax1Y = TUQ('ch4_e',forx,0.1,True,False)[0]
    ax1X = TUQ('ch4_e',forx,0.1,True,False)[1]
    ax1_p = KD(ax1Y,ax1X,'CH4_e',Xname)[0]
    ax1_param = KD(ax1Y,ax1X,'CH4_e',Xname)[1]
    ax2Y = TUQ('ch4_d',forx,0.1,True,False)[0]
    ax2X = TUQ('ch4_d',forx,0.1,True,False)[1]
    ax2_p = KD(ax2Y,ax2X,'CH4_d',Xname)[0]
    ax2_param = KD(ax2Y,ax2X,'CH4_d',Xname)[1]
    ax3Y = TUQ('ch4_e',forx,1.5,False,False)[0]
    ax3X = TUQ('ch4_e',forx,1.5,False,False)[1]
    ax3_p = KD(ax3Y,ax3X,'CH4_e',Xname)[0]
    ax3_param = KD(ax3Y,ax3X,'CH4_e',Xname)[1]
    ax4Y = TUQ('ch4_d',forx,1.5,False,False)[0]
    ax4X = TUQ('ch4_d',forx,1.5,False,False)[1]
    ax4_p = KD(ax4Y,ax4X,'CH4_d',Xname)[0]
    ax4_param = KD(ax4Y,ax4X,'CH4_d',Xname)[1]
    fig=plt.figure(figsize=(14,5),dpi=300)
    ax1=fig.add_subplot(241) 
    ax1.scatter(ax1X,ax1Y,s=50,c='#336666',alpha=0.5,marker='.')
    sns.regplot(ax1X,ax1Y,ax=ax1,scatter=False,ci=0,color = '#336666')
    mark1 = pvaluestr(float(ax1_p)) + '| Slope {'+str(np.round(float(ax1_param),2))+ '}'
    ax1.annotate( mark1  ,xy=(np.quantile(ax1X,0.08),np.quantile(ax1Y,0.3)),xytext=(np.min(ax1X)+0.1,np.quantile(ax1Y,0.8)))
    ax1.set_title('Lake| Net effect of ' + Xname + ' on CH4E'    ,fontdict=font_Ylae)
    ax1.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
    ax1.set_ylabel('Ebullition CH4 flux mg_CH4-C_m_2_d_1(logarithm)',fontdict=font_Yble)
    ax2=fig.add_subplot(242) 
    ax2.scatter(ax2X,ax2Y,s=50,c='#669999',alpha=0.5,marker='.')
    sns.regplot(ax2X,ax2Y,ax=ax2,scatter=False,ci=0,color = '#669999')
    mark2 = pvaluestr(float(ax2_p)) + '| Slope {'+str(np.round(float(ax2_param),2))+ '}'
    ax2.annotate( mark2  ,xy=(np.quantile(ax2X,0.08),np.quantile(ax2Y,0.3)),xytext=(np.min(ax2X)+0.1,np.quantile(ax2Y,0.8)))
    ax2.set_title('Lake| Net effect of ' + Xname + ' on CH4D'    ,fontdict=font_Ylae)
    ax2.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
    ax2.set_ylabel('Diffusio CH4 flux mg_CH4-C_m_2_d_1(logarithm)',fontdict=font_Yble)
    ax3=fig.add_subplot(243) 
    ax3.scatter(ax3X,ax3Y,s=50,c='#339999',alpha=0.5,marker='.')
    sns.regplot(ax3X,ax3Y,ax=ax3,scatter=False,ci=0,color = '#339999')
    mark3 = pvaluestr(float(ax3_p)) + '| Slope {'+str(np.round(float(ax3_param),2))+ '}'
    ax3.annotate( mark3  ,xy=(np.quantile(ax3X,0.08),np.quantile(ax3Y,0.3)),xytext=(np.min(ax3X)+0.1,np.quantile(ax3Y,0.8)))
    ax3.set_title('Reservoir| Net effect of ' + Xname + ' on CH4E'    ,fontdict=font_Ylae)
    ax3.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
    ax3.set_ylabel('Ebullition CH4 flux mg_CH4-C_m_2_d_1(logarithm)',fontdict=font_Yble)
    ax4=fig.add_subplot(244) 
    ax4.scatter(ax4X,ax4Y,s=50,c='#336699',alpha=0.5,marker='.')
    sns.regplot(ax4X,ax4Y,ax=ax4,scatter=False,ci=0,color = '#336699')
    mark4 = pvaluestr(float(ax4_p)) + '| Slope {'+str(np.round(float(ax4_param),2))+ '}'
    ax4.annotate( mark4  ,xy=(np.quantile(ax4X,0.08),np.quantile(ax4Y,0.3)),xytext=(np.min(ax4X)+0.1,np.quantile(ax4Y,0.8)))
    ax4.set_title('Reservoir| Net effect of ' + Xname + ' on CH4D'    ,fontdict=font_Ylae)
    ax4.set_xlabel(Xname + ' (logarithm)',fontdict=font_Ylae)
    ax4.set_ylabel('Diffusio CH4 flux mg_CH4-C_m_2_d_1(logarithm)',fontdict=font_Yble)
    plt.tight_layout()
    return 















