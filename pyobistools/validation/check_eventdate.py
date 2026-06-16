import pandas as pd
import re


pattern = r'^\d{4}(-\d{2}(-\d{2}([T|\s]\d{2}(:\d{2}(:\d{2})?)?(Z|([+-]\d{2}:?(\d{2})?))?)?)?)?$'

def check_eventdate(data: pd.DataFrame, level='error'):
    """Validates the eventDate column.

    Args:
        data (pd.DataFrame): Event core file as a dataframe
    """
    if 'eventDate' not in data.columns:
        return pd.DataFrame({
            'level': 'error',
            'message': 'Column eventDate missing'
        })
    report_df = pd.DataFrame(columns=['level', 'row', 'field', 'message'])
    for idx, row in data.iterrows():
        valid = check_date(row.eventDate)    
        
        if valid:
            message = f"eventDate '{row.eventDate}' is valid."
        else:
            message = f"eventDate '{row.eventDate}' does not seem to be a valid date."
        
        report_df = pd.concat([report_df, pd.DataFrame(data={
            'level': ['report' if valid else 'error'],
            'row': [idx],
            'field': ['eventDate'],
            'message': [message]
        })])
    
    if level == 'error':
        report_df = report_df.loc[report_df['level'] == 'error'].copy()
    report_df.reset_index(drop=True, inplace=True)
    return report_df


def check_date(date: str):
    """Checks if date is valid.

    Args:
        date (str): the date to be validated

    Returns:
        bool: Whether the date is valid or not
    """
    print(date)
    if date is None or date == '' or pd.isna(date):
        return False
    
    # Split date to check if its an interval
    dates = date.split('/')
    
    if len(dates) == 1:
        return re.match(pattern, date) is not None
    elif len(dates) == 2:
        first_match = re.match(pattern, dates[0])
        second_match = re.match(pattern, dates[1])
        if first_match and second_match:
            return True
        # Checks for interval notation
        elif first_match and len(dates[0]) > len(dates[1]):
            first = dates[0]
            second = dates[1]
            # Get the higher level date info from the first date and prepend it to the second date
            second = first[0:(len(first) - len(second))] + second
            # Check if the modified second date is valid
            return re.match(pattern, second) is not None
    return False
