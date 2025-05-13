import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='Program Budget Dashboard',page_icon=':chart_with_upwards_trend:',layout='wide')

st.markdown(
    '''
    # Program Budget Dashboard
    Each section provides analytics that may be useful for your budget review and tracking.
    '''
)

st.markdown(
    '''
    ## Salary by Employee
    Upload your "Salary By Employee [Date].xlsx" file to see analytics.
    '''
)

salary_by_employee_file = st.file_uploader("Upload file (.xlsx)", type=["xlsx"])

pivot_values_option = st.selectbox('Select cost or hours:',options=['Cost','Hours'])
if pivot_values_option == 'Hours':
    pivot_values = 'ActualQty'
else:
    pivot_values = 'Cost'

if salary_by_employee_file is not None:
    try:
        df_salary_by_employee = pd.read_excel(salary_by_employee_file,sheet_name='Sheet1')
        st.write('Data loaded:')
        st.dataframe(df_salary_by_employee)

        

        df_salary_by_employee['FundingSourceType'] = df_salary_by_employee['FundingSource'].apply(lambda x: x[:2])
        df_sbe_pivot = df_salary_by_employee.pivot_table(values=pivot_values,columns='FundingSourceType',index='ResourceName',fill_value=0,aggfunc='sum')
        df_sbe_pivot['Total'] = df_sbe_pivot.sum(axis=1)
        df_sbe_pivot = df_sbe_pivot[df_sbe_pivot['Total'] > 0]

        st.write(f'Total of employee {pivot_values_option.lower()} by funding source type:')
        st.dataframe(df_sbe_pivot)

        df_sbe_pivot_percent = 100*df_sbe_pivot.div(df_sbe_pivot['Total'],axis=0)
        df_sbe_pivot_percent = df_sbe_pivot_percent.apply(lambda x: np.round(x,decimals=0)).astype(int)

        st.write(f'Percent of employee {pivot_values_option.lower()} by funding source type:')
        st.dataframe(df_sbe_pivot_percent)

    except Exception as e:
        st.error(f"Error reading the file: {e}")
else:
    st.info("Please upload an XLSX file.")


