#!/usr/bin/env python3
"""
Extract running data from Garmin Connect using the `garminconnect` library, handling 2FA via a user prompt,
and perform exploratory analysis to uncover patterns, including weekly trends, heart rate analysis, and anomaly detection.

Requirements:
    pip install garminconnect pandas click

Usage:
    export GARMIN_USERNAME="your_username"
    export GARMIN_PASSWORD="your_password"
    python extract_running_data_garmin_connect.py \
        --start-date 2025-01-01 \
        --end-date 2025-05-16 \
        --output runs.csv
"""
import os
import datetime
import pandas as pd
import click
from garminconnect import Garmin, GarminConnectConnectionError, GarminConnectAuthenticationError


def two_factor_callback():
    """
    Prompt the user for the Garmin 2FA verification code.
    """
    return click.prompt('Enter Garmin 2FA code', hide_input=False)


def fetch_runs(client, start_date, end_date, limit=1000):
    """
    Fetch activities and filter for runs between start_date and end_date,
    extracting key metrics including heart rate.
    """
    activities = client.get_activities(start_date, limit=limit)
    runs = []
    for act in activities:
        if act.get('activityType', {}).get('typeKey') == 'running':
            details = client.get_activity_details(act['activityId'])
            summary = details.get('activitySummary', {})
            local_start = datetime.datetime.fromisoformat(summary['startTimeLocal'])
            if start_date <= local_start <= end_date:
                runs.append({
                    'id': act['activityId'],
                    'name': summary.get('activityName', ''),
                    'start_time': summary['startTimeLocal'],
                    'distance_km': summary.get('distance', 0) / 1000,
                    'duration_s': summary.get('duration', 0),
                    'calories': summary.get('calories', 0),
                    'avg_hr': summary.get('averageHR', None),
                    'max_hr': summary.get('maxHR', None),
                })
    return pd.DataFrame(runs)


def analyze_runs(df):
    """
    Perform exploratory analysis on the runs DataFrame and print summaries,
    including weekly distance & heart rate trends, and detect anomalies in heart rate.
    """
    # Prepare
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['pace_s_per_km'] = df['duration_s'] / df['distance_km']
    df.set_index('start_time', inplace=True)

    # Overall stats
    total_runs = len(df)
    total_distance = df['distance_km'].sum()
    avg_distance = df['distance_km'].mean()
    avg_pace = df['pace_s_per_km'].mean()
    fastest_pace = df['pace_s_per_km'].min()
    longest_run = df['distance_km'].max()
    avg_hr = df['avg_hr'].dropna().mean() if 'avg_hr' in df else None
    max_hr_overall = df['max_hr'].dropna().max() if 'max_hr' in df else None
    avg_max_hr = df['max_hr'].dropna().mean() if 'max_hr' in df else None
    corr_pace_hr = df[['pace_s_per_km', 'avg_hr']].dropna().corr().iloc[0,1] if 'avg_hr' in df else None

    click.echo(f"\n=== Run Summary ===")
    click.echo(f"Total runs: {total_runs}")
    click.echo(f"Total distance: {total_distance:.2f} km")
    click.echo(f"Average distance: {avg_distance:.2f} km")
    click.echo(f"Average pace: {int(avg_pace//60)}:{int(avg_pace%60):02d} min/km")
    click.echo(f"Fastest pace: {int(fastest_pace//60)}:{int(fastest_pace%60):02d} min/km")
    click.echo(f"Longest run: {longest_run:.2f} km")
    if avg_hr is not None:
        click.echo(f"Average heart rate: {avg_hr:.0f} bpm")
    if max_hr_overall is not None:
        click.echo(f"Highest recorded HR: {max_hr_overall} bpm")
    if corr_pace_hr is not None:
        click.echo(f"Pace vs Avg HR correlation: {corr_pace_hr:.2f}")

    # Weekly distance trends
    weekly_dist = df['distance_km'].resample('W').sum()
    click.echo(f"\nWeekly Distance Trend (km per week):")
    for week_start, dist in weekly_dist.items():
        click.echo(f"  {week_start.date()} – {dist:.2f}")

    # Weekly heart rate trends
    if 'avg_hr' in df and not df['avg_hr'].dropna().empty:
        weekly_hr = df['avg_hr'].resample('W').mean()
        click.echo(f"\nWeekly Average Heart Rate (bpm):")
        for week_start, hr in weekly_hr.items():
            click.echo(f"  {week_start.date()} – {hr:.1f}")

    # Anomaly detection for average heart rate
    if 'avg_hr' in df and df['avg_hr'].dropna().shape[0] > 1:
        hr_series = df['avg_hr'].dropna()
        hr_mean = hr_series.mean()
        hr_std = hr_series.std()
        df['avg_hr_z'] = (df['avg_hr'] - hr_mean) / hr_std
        anomalies_avg = df[df['avg_hr_z'].abs() > 2]
        click.echo(f"\n=== Avg HR Anomalies (|z|>2) ===")
        if anomalies_avg.empty:
            click.echo("No significant anomalies detected in average heart rate.")
        else:
            for ts, row in anomalies_avg.iterrows():
                click.echo(f"{ts.date()}: avg HR={row['avg_hr']} bpm (z={row['avg_hr_z']:.2f})")

    # Anomaly detection for max heart rate
    if 'max_hr' in df and df['max_hr'].dropna().shape[0] > 1:
        max_hr_series = df['max_hr'].dropna()
        max_hr_mean = max_hr_series.mean()
        max_hr_std = max_hr_series.std()
        df['max_hr_z'] = (df['max_hr'] - max_hr_mean) / max_hr_std
        anomalies_max = df[df['max_hr_z'].abs() > 2]
        click.echo(f"\n=== Max HR Anomalies (|z|>2) ===")
        if anomalies_max.empty:
            click.echo("No significant anomalies detected in maximum heart rate.")
        else:
            for ts, row in anomalies_max.iterrows():
                click.echo(f"{ts.date()}: max HR={row['max_hr']} bpm (z={row['max_hr_z']:.2f})")

@click.command()
@click.option('--username', '-u', envvar='GARMIN_USERNAME', prompt='Garmin username', help='Garmin Connect username')
@click.option('--password', '-p', envvar='GARMIN_PASSWORD', prompt='Garmin password', hide_input=True, help='Garmin Connect password')
@click.option('--start-date', default=(datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d'),
              help='Start date (YYYY-MM-DD)')
@click.option('--end-date', default=datetime.datetime.now().strftime('%Y-%m-%d'),
              help='End date (YYYY-MM-DD)')
@click.option('--output', '-o', default='running_data.csv', help='CSV file to save output')
def main(username, password, start_date, end_date, output):
    """
    Authenticate with Garmin Connect (handling 2FA), fetch running activities, save to CSV, and analyze.
    """
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)

    try:
        client = Garmin(username, password)
        client.login(two_factor_callback=two_factor_callback)
    except GarminConnectAuthenticationError as auth_err:
        click.echo(f"[AUTH ERROR] {auth_err}")
        raise SystemExit(1)
    except GarminConnectConnectionError as conn_err:
        click.echo(f"[CONNECTION ERROR] {conn_err}")
        raise SystemExit(1)

    df = fetch_runs(client, start, end)
    if df.empty:
        click.echo("No running activities found in the specified date range.")
        return

    click.echo(df)
    df.to_csv(output, index=False)
    click.echo(f"Saved {len(df)} running activities to {output}")

    analyze_runs(df)

if __name__ == '__main__':
    main()
