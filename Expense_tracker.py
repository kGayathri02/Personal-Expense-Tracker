import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

def data_clean():
    
    df= Path(__file__).parents[1] / 'Downloads/expense_data_1.csv'

    df= df.drop(columns= ['Subcategory','Note.1','Account.1',])

    df.fillna({'Note': 'Random'}, inplace=True)

    df.loc[df['Currency']== 'USD', 'Amount'] = 1120.72

    df= df.drop(columns= ['INR', 'Currency'])

    df['Date'] = pd.to_datetime(df['Date'])
    df['Year']= df['Date'].dt.year
    df['Month']= df['Date'].dt.month

    return df

df = data_clean()

income_df= df[df['Income/Expense'] == 'Income']
expense_df= df[df['Income/Expense'] == 'Expense']  
Total_income = income_df['Amount'].sum()
Total_expense = expense_df['Amount'].sum()
net_income= Total_income - Total_expense

    
tab1,tab2,tab3,tab4,tab5,tab6,tab7= st.tabs(['Data Table', 'Income & Expense', 'Category-wise Breakdown', 'Highest/Lowest Spending', 'Income-Expense Ratio','Cash-flow Over Time', 'Conclusion'])

with tab1:
    st.subheader('Showing Data Table')
    option1= st.selectbox('Choose Data to Display', ['Show Data', 'Income Data', 'Expense Data'])
    if option1=='Show Data':
        st.write('All Data')
        st.dataframe(df)

    elif option1=='Income Data':
        st.write('Income Data')
        st.dataframe(income_df)
        st.write(f'Total Income: {Total_income}')
        st.write(f'Net Income: {net_income}')
        
    elif option1=='Expense Data':
        st.write('Expense Data')
        st.dataframe(expense_df)
        st.write(f'Total Expense: {Total_expense}')

with tab2:
    st.subheader('Previous Month Income & Expense')
    income_monthly = income_df.groupby(['Year', 'Month'])['Amount'].sum().reset_index()
    expense_monthly = expense_df.groupby(['Year', 'Month'])['Amount'].sum().reset_index()

    # Preview monthly income and expense
    st.write("\nMonthly Income:")
    st.write(income_monthly)

    st.write("\nMonthly Expenses:")
    st.write(expense_monthly)

with tab3:
    st.subheader('Summarize how much is spent on different categories like food, transportation, etc., over time.')
    result = df.groupby(by=['Category', 'Income/Expense']).agg({
    'Amount': 'sum',  
    'Month': 'count'   
    }).reset_index()
    st.dataframe(result)
    st.write('Note: How many time the person spend/recieve money for 5 Month.')

    st.subheader('Analyze how your spending habits evolve over time, such as comparing monthly spending in specific categories.')
    result2= df.groupby(by=['Note','Category', 'Income/Expense']).agg({
        'Amount':'sum',
        'Month':'count'
    }).reset_index()
    result2 = result2.sort_values(by='Amount', ascending=False)
    st.dataframe(result2)


with tab4:
    st.header('Identify which months or categories have the highest and lowest expenditures.')

    select_option= st.selectbox('Choose the Option:',['By Category', 'By Month'])
    
    if select_option== 'By Category':

        st.subheader('The Highest and Lowest Expenditures by Category')
        category_expenses = expense_df.groupby('Category')['Amount'].sum().reset_index()
        
        highest_expense_category = category_expenses.sort_values(by='Amount', ascending=False).head(1)
        lowest_expense_category = category_expenses.sort_values(by='Amount', ascending=True).head(1)

        st.dataframe(highest_expense_category)
        st.dataframe(lowest_expense_category)
    
    elif select_option== 'By Month':

        st.subheader('The Highest and Lowest Expenditures by Month')
        monthly_expenses = expense_df.groupby('Month')['Amount'].sum().reset_index()

        highest_expense_month = monthly_expenses.sort_values(by='Amount', ascending=False).head(1)
        lowest_expense_month = monthly_expenses.sort_values(by='Amount', ascending=True).head(1)

        st.dataframe(highest_expense_month)
        st.dataframe(lowest_expense_month)
    
    st.markdown('''This shows that food is the largest spending category, and January had the highest overall expenditure. 
                Conversely, the lowest spending occurred in the category of gifts and the month of March.''')

with tab5:
    st.header('Track the proportion of income spent to understand how well you’re managing your finances.')
    st.subheader('Track Proportion of Income Spent by Month')
        # Sum income and expense for each month
    monthly_income = income_df.groupby('Month')['Amount'].sum().reset_index(name='Total_Income')
    monthly_expense = expense_df.groupby('Month')['Amount'].sum().reset_index(name='Total_Expense')

    # Merge the two dataframes to calculate proportion
    monthly_finances = pd.merge(monthly_income, monthly_expense, on='Month', how='outer')

    # Calculate the proportion of income spent
    monthly_finances['Proportion_Spent (%)'] = (monthly_finances['Total_Expense'] / monthly_finances['Total_Income']) * 100

    st.dataframe(monthly_finances)

    st.markdown('''
- Month 1: You spent 105.29% of your income, meaning expenses were higher than income.
- Month 2: You spent 98.16% of your income, close to balanced.
- Month 3: You spent 87.5% of your income, staying under budget.
- Month 11: You spent 90.44% of your income, showing good financial control.
- Month 12: You spent 132.69% of your income, significantly exceeding your earnings.

- In summary, except for months 1 and 12, spending is relatively under control.''')

with tab6:
    st.header('Visualize cash flow trends to monitor consistency in income and expenses.')
    st.subheader('Cash Flow Trends by Month')   
    monthly_income = income_df.groupby('Month')['Amount'].sum().reset_index(name='Total_Income')
    monthly_expense = expense_df.groupby('Month')['Amount'].sum().reset_index(name='Total_Expense')

    # Merge the income and expense data on 'Month'
    cash_flow = pd.merge(monthly_income, monthly_expense, on='Month', how='outer')

    # Plot income and expense trends over time
    plt.figure(figsize=(10,6))
    plt.plot(cash_flow['Month'], cash_flow['Total_Income'], label='Income', marker='o', color='green')
    plt.plot(cash_flow['Month'], cash_flow['Total_Expense'], label='Expense', marker='o', color='red')

    plt.title('Cash Flow Trends: Monthly Income vs Expense')
    plt.xlabel('Month')
    plt.ylabel('Amount (INR)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    st.markdown('''Your spending patterns show fluctuations where expenses were close to income in some months but exceeded income in others. 
    Here’s a brief summary:
- Close to Income: In certain months, your expenses were nearly equal to your income, indicating a balanced financial situation. This could suggest careful spending during these times.
- Exceeding Income: In other months, expenses surpassed income, which could lead to financial strain. This indicates a need for better budget management or adjustment in spending habits during those periods.''')

with tab7:
    st.header('Detailed Report')
    st.subheader('Report based on Income & Expense')
    st.markdown('''
- In November 2021 and February 2022, income exceeded expenses which is surplus.
- In December 2021 and January 2022  shows shortage where expenses is higher than icnome.
- Overall, financial handling seems inconsistent, with spending being higher than income in two of the four months.''')

    st.subheader('Report based on Category-wise Breakdown')
    st.write('how much is spent on different categories like food, transportation, etc., over time:')
    st.markdown('''
- Food is the largest expense, making up a major portion of spending with ₹24,502.48 over 156 transactions, indicating frequent  expenditures in this category.
- Transportation and Household also show notable spending with ₹9,203.80 and ₹12,188 respectively, over fewer but meaningful transactions.
- Other categories like Social Life, Apparel, and Other expenses also reflect smaller but consistent outflows.
- Education, Self-development, Beauty, and Gift are minimal expenses, with just one or few transactions each.''')
    st.markdown('''For income:
- The majority of income comes from Other Income (₹32,751), followed by Allowance (₹14,000) and Salary (₹8,000).''')
    

    st.write('spending habits evolve over time, such as comparing monthly spending in specific categories:')
    st.markdown('''
- Food is consistently one of the highest expenditure categories, with frequent transactions such as lunch, dinner, and snacks. This indicates a regular habit of eating out or purchasing food.
- Household expenses, like rent and other essentials, appear less frequently but involve larger amounts, signifying significant but less frequent spending.
- Transportation shows regular spending, often for travel or commuting purposes.
- Apparel, Social Life, and Education show some occasional but notable expenses, often tied to specific events like purchasing clothing or social activities.
- Other Income (such as money from family members) is a major source of income, with occasional larger sums boosting the cash flow.
- In summary, food and transportation represent regular expenses, while categories like household and apparel have larger, but less frequent outflows. Income primarily comes from allowances and occasional contributions from family, highlighting reliance on these sources.''')

    st.header('Overall Report')
    st.markdown('''
- Budgeting: Consider setting a monthly budget to limit expenses, particularly in months where spending tends to rise.
- Monitoring: Regularly track income and expenses to identify trends and adjust spending accordingly.
- Savings Goal: Aim to save a portion of your income each month to build a financial cushion for months with higher expenses.
''')
