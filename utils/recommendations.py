def generate_recommendations(df):
    """
    Generates smart recommendations from downtime, issue patterns & performance
    """

    recs = []

    # 1. High downtime machines
    machine_downtime = df.groupby("Machine_Type")["Downtime_Hours"].sum()
    worst_machine = machine_downtime.idxmax()
    worst_machine_hours = machine_downtime.max()

    recs.append(
        f"Machine **{worst_machine}** has the highest downtime ({worst_machine_hours:.2f} hrs). Consider preventive maintenance."
    )

    # 2. Most problematic issue type
    issue_downtime = df.groupby("Issue_Type")["Downtime_Hours"].sum()
    worst_issue = issue_downtime.idxmax()
    worst_issue_hours = issue_downtime.max()

    recs.append(
        f"The issue type **{worst_issue}** contributes the most downtime ({worst_issue_hours:.2f} hrs). Investigate root causes."
    )

    # 3. Shift performance problems
    shift_downtime = df.groupby("Shift")["Downtime_Hours"].sum()
    worst_shift = shift_downtime.idxmax()
    worst_shift_hours = shift_downtime.max()

    recs.append(
        f"**{worst_shift} Shift** has the highest downtime ({worst_shift_hours:.2f} hrs). Training or workflow review recommended."
    )

    # 4. Increasing monthly downtime
    month_downtime = df.groupby("Month")["Downtime_Hours"].sum()
    if month_downtime.iloc[-1] > month_downtime.iloc[0]:
        recs.append(
            "Downtime is **increasing month-over-month**. Review maintenance schedules and inspection routines."
        )

    # 5. High cost impact
    df["Cost"] = df["Downtime_Hours"] * 1200
    total_cost = df["Cost"].sum()

    if total_cost > 50000:
        recs.append(
            f"Downtime cost exceeded **₹{total_cost:.2f}**. Priority action needed to reduce financial loss."
        )

    # 6. Health score monitoring
    utilization = df["Actual_Work_Hours"].sum() / df["Planned_Work_Hours"].sum()

    if utilization < 0.5:
        recs.append(
            "Low utilization detected (below 50%). Consider improving machine scheduling & production planning."
        )

    # 7. Frequent downtime events
    frequent_downtime = df[df["Downtime_Hours"] > 2].shape[0]
    if frequent_downtime > 5:
        recs.append(
            "Frequent long downtime events detected. Investigate repeated failure sources."
        )

    # Default if no recommendations
    if len(recs) == 0:
        recs.append("All systems performing normally. No critical insights.")

    return recs
