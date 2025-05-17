################################################
# LIBRARIES
################################################
import pandas as pd
from dask_expr.diagnostics import analyze

################################################
# SETTINGS
################################################
pd.set_option('display.max_columns', None)
pd.set_option("display.width", 500)




################################################
# FUNCTIONS
################################################
def load_excel_data(filepath):
    """
    Load a dataset from an Excel file.

    Parameters
    ----------
    filepath : str
        Path to the Excel (.xlsx) file containing the dataset.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the loaded dataset.
    """
    return pd.read_excel(filepath)


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Value Counts #####################")
    print(dataframe.nunique())
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


def explore_data(df, group_vars, target_var):
    """
    Perform basic exploratory data analysis by printing counts and aggregated metrics.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to explore.
    group_vars : list of str
        List of categorical columns to group by.
    target_var : str
        Target variable to aggregate.

    Returns
    -------
    None
        This function only prints output and does not return anything.
    """
    for var in group_vars:
        print(f"{var} counts:\n", df[var].value_counts(), "\n")
        print(f"{var} mean of {target_var}:\n", df.groupby(var)[target_var].mean(), "\n")
        print(f"{var} sum of {target_var}:\n", df.groupby(var)[target_var].sum(), "\n")
        print("######################################################")

    print("Group-wise mean:")
    print(df.groupby(group_vars)[target_var].mean())


def grab_col_names(dataframe, cat_th=10,  car_th=20):
    """
        Returns the names of categorical, numerical, and categorical but cardinal variables in a given DataFrame.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The DataFrame from which to extract variable names.
        cat_th : int or float, optional
            Threshold for determining numerical variables that are considered categorical (default is 10).
        car_th : int or float, optional
            Threshold for determining categorical variables that are considered cardinal (default is 20).

        Returns
        -------
        cat_cols : list of str
            List of categorical variable names.
        num_cols : list of str
            List of numerical variable names.
        cat_but_car : list of str
            List of variables that appear categorical but are actually cardinal.

        Notes
        -----
        - The union of `cat_cols`, `num_cols`, and `cat_but_car` equals the total number of columns in the DataFrame.
        - Variables in `num_but_cat` are included in `cat_cols`.
        - `cat_cols` excludes variables classified as `cat_but_car`.
    """

    # cat_cols, cat_but_car
    cat_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"]]

    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < 10 and dataframe[col].dtypes in ["int", "float"]]

    cat_but_car = [col for col in dataframe.columns if
                   dataframe[col].nunique() > 20 and str(dataframe[col].dtypes) in ["category", "object"]]

    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes in ["int", "float"]]
    num_cols = [col for col in num_cols if col not in cat_cols]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f'cat_cols: {len(cat_cols)}')
    print(f'num_cols: {len(num_cols)}')
    print(f'cat_but_car: {len(cat_but_car)}')
    print(f'num_but_cat: {len(num_but_cat)}')

    return cat_cols, num_cols, cat_but_car


def categorize_column(df, column, bins, labels, new_col_name):
    """
    Categorize a numerical column into categorical bins.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    column : str
        Name of the column to categorize.
    bins : list of int or float
        Bin edges.
    labels : list of str
        Labels for the resulting categories.
    new_col_name : str
        Name for the new column to be created.

    Returns
    -------
    pd.DataFrame
        Modified DataFrame with the new categorized column added.
    """
    new_df = df.copy()
    new_df[new_col_name] = pd.cut(df[column], bins=bins, labels=labels)
    return new_df


def group_and_aggregate(df, group_vars, target_var):
    """
    Aggregate a target variable by specified group variables.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    group_vars : list of str
        Columns to group by.
    target_var : str
        Target variable for aggregation.

    Returns
    -------
    pd.DataFrame
        Aggregated DataFrame with mean target values for each group.
    """
    return df.groupby(group_vars).agg({target_var: "mean"}).reset_index()


def create_level_based_id(df, group_vars, new_col_name):
    """
    Create a level-based identifier by concatenating categorical variables.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    group_vars : list of str
        List of columns to concatenate.
    new_col_name : str
        Name for the new identifier column.

    Returns
    -------
    pd.DataFrame
        DataFrame with an additional column representing level-based ID.
    """
    df_copy = df.copy()

    df_copy[new_col_name] = ""

    for i, col in enumerate(group_vars):
        if i + 1 != len(group_vars):
            df_copy[new_col_name] += df[col] +  "_"
        else:
            df_copy[new_col_name] += df[col]

    # Second way:
    #df_copy[new_col_name] = df_copy[group_vars].apply(lambda row: "_".join(row).upper(), axis=1)

    return df_copy


def assign_segments(df, target_var, new_col_name="Segment", n_segments=4, labels=["D", "C", "B", "A"]):
    """
    Assign segments to rows based on quantiles of the target variable.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the target variable.
    target_var : str
        Variable to base segmentation on.
    new_col_name : str, optional
        Name of the new segment column. Default is 'Segment'.
    n_segments : int, optional
        Number of segments (default 4).
    labels : list of str, optional
        Labels to assign to each segment.

    Returns
    -------
    pd.DataFrame
        DataFrame with an additional segment column.
    """
    df_copy = df.copy()

    df_copy[new_col_name] = pd.qcut(df_copy[target_var], q=n_segments, labels=labels)

    return df_copy


def estimate_segment_value(df, persona):
    """
    Estimate value statistics for a given identifier from its assigned segment.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the segments and target variable.
    persona : str
        The identifier value to look up.

    Returns
    -------
    tuple
        Segment label (str) and a DataFrame with average, max, and total of the target variable.
    """
    segment = df[df["sales_level_based"].str.upper() == persona.upper()]["Segment"].values[0]
    summary = df[df["Segment"] == segment].groupby("Segment").agg(
        Avg_Value=("Price", "mean"),
        Min_Value=("Price", "min"),
        Max_Value=("Price", "max"),
        Total_Value=("Price", "sum")
    ).reset_index()

    print(f"{persona.upper()}: \n", summary[summary["Segment"] == segment])

    return segment, summary.reset_index()




################################################
# DATA LOADING
################################################
df = load_excel_data("Case_Study_3/gezinomi_tanıtım/miuul_gezinomi.xlsx")




################################################
# GENERAL OVERVIEW
################################################
# General look to data
check_df(df)

# Exploring the statistics
explore_data(df, group_vars=["ConceptName", "SaleCityName"], target_var="Price")




################################################
# DATA TYPE ADJUSTMENTS
################################################
# To avoid future conflicts in categorizing we adjust the data type
df["SaleId"] = df["SaleId"].astype(dtype="object")




################################################
# HANDLING MISSING DATA
################################################
# Since target value is empty we drop the NaN values.
df.dropna(inplace=True)




################################################
# FEATURE CREATING
################################################
# Creating `EB_Score`
bins = [-1, 7, 30, 90, 180, 900]
labels = ["Last_Minuters", "Potential_Planners", "Planners", "Early_Birds", "Promotioners"]

agg_df = categorize_column(df, "SaleCheckInDayDiff", bins, labels, "EB_Score")


# Creating `sales_level_based` variable
agg_df = create_level_based_id(agg_df, ["SaleCityName", "ConceptName", "Seasons"], "sales_level_based")


# Creating `Segments` variable
agg_df = assign_segments(agg_df, "Price", new_col_name="Segment", n_segments=4, labels=["D", "C", "B", "A"])


# Checking the dataframe
check_df(agg_df)




################################################
# ANALYZES
################################################
# Analyzing the EB_Score
analyze_df = group_and_aggregate(agg_df, ["SaleCityName", "ConceptName", "EB_Score"], target_var="Price").sort_values(by="Price", ascending=False)

# The NaN values are result of 0 dividing.
agg_df[(agg_df["SaleCityName"] == "Antalya") & (agg_df["ConceptName"] == "Oda + Kahvaltı") & (agg_df["EB_Score"] == "Promotioners")]
analyze_df = analyze_df["Price"].fillna(0)


# Segment Analyze
segment_df = agg_df.groupby(["Segment"]).agg(
    Avg_Value=("Price", "mean"),
    Min_Value=("Price", "min"),
    Max_Value=("Price", "max"),
    Total_Value=("Price", "sum")
).sort_values(by="Avg_Value", ascending=False).reset_index()


# Estiamting the profit
segment, estimate_df = estimate_segment_value(agg_df, "antalya_herşey dahil_low") # Enter `persona` as your desire.