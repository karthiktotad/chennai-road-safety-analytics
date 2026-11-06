"""
Exploratory Data Analysis (EDA) Module.
Generates publication-quality visualizations answering 12 core road safety research questions.
Distinguishes absolute incident counts from severity rates.
Saves figures to results/visualizations/ and synthesizes findings in results/reports/.
"""

import logging
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from config.settings import (
    PROCESSED_DATA_DIR, VISUALIZATIONS_DIR, REPORTS_DIR
)

# Professional visualization styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10
plt.rcParams["figure.dpi"] = 300

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class ChennaiAccidentEDA:
    """Executes systematic exploratory data analysis for Chennai road crashes."""

    def __init__(self):
        self.annual_df = pd.read_csv(PROCESSED_DATA_DIR / "chennai_annual_crash_severity_preprocessed.csv")
        self.weather_df = pd.read_csv(PROCESSED_DATA_DIR / "chennai_daily_weather_preprocessed.csv")
        self.modeling_df = pd.read_csv(PROCESSED_DATA_DIR / "chennai_accident_severity_modeling_dataset.csv")
        self.vis_dir = VISUALIZATIONS_DIR
        self.rep_dir = REPORTS_DIR

    def plot_01_accident_trends_year(self):
        """1. Accident trends by year (1998-2025): Total, Fatal, Grievous, and Severity Rate."""
        fig, ax1 = plt.subplots(figsize=(10, 5))

        color1 = "#1f77b4"
        color2 = "#d62728"
        color3 = "#ff7f0e"

        ax1.plot(self.annual_df["year"], self.annual_df["total_accidents"], marker="o", color=color1, linewidth=2, label="Total Recorded Accidents")
        ax1.plot(self.annual_df["year"], self.annual_df["severe_accidents"], marker="s", color=color2, linewidth=2, label="Severe Accidents (Fatal + Grievous)")
        ax1.plot(self.annual_df["year"], self.annual_df["fatal_accidents"], marker="^", color=color3, linestyle="--", label="Fatal Accidents")
        ax1.set_xlabel("Reporting Year (1998–2025)")
        ax1.set_ylabel("Annual Incident Count", color="#333333")
        ax1.tick_params(axis="y")
        ax1.grid(True, linestyle=":", alpha=0.6)

        # Secondary axis for Severity Rate (%)
        ax2 = ax1.twinx()
        color4 = "#2ca02c"
        ax2.plot(self.annual_df["year"], self.annual_df["severity_rate"] * 100, color=color4, linewidth=2.5, linestyle="-.", label="Severity Rate (% Severe)")
        ax2.set_ylabel("Severity Rate (% of Total Accidents)", color=color4)
        ax2.tick_params(axis="y", labelcolor=color4)
        ax2.set_ylim(0, 100)

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True)

        plt.title("Chennai Road Accident Volume & Severity Progression (1998–2025)\nDistinguishing Absolute Crash Counts from Crash Severity Ratio", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_01_accident_trends_year.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_02_accident_distribution_month(self):
        """2. Accident distribution by month & seasonal exposure."""
        self.modeling_df["month"] = pd.to_datetime(self.modeling_df["accident_date"]).dt.month
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        m_stats = self.modeling_df.groupby("month").agg(
            total=("accident_id", "count"),
            severe=("severe_accident", "sum")
        ).reset_index()
        m_stats["non_severe"] = m_stats["total"] - m_stats["severe"]
        m_stats["severity_rate"] = m_stats["severe"] / m_stats["total"] * 100
        m_stats["month_name"] = [month_names[m - 1] for m in m_stats["month"]]

        fig, ax1 = plt.subplots(figsize=(9, 4.8))
        x = np.arange(len(m_stats))
        width = 0.55

        ax1.bar(x, m_stats["severe"], width, label="Severe (Fatal/Grievous)", color="#d95f02", alpha=0.9)
        ax1.bar(x, m_stats["non_severe"], width, bottom=m_stats["severe"], label="Non-Severe (Minor/None)", color="#7570b3", alpha=0.8)
        ax1.set_xlabel("Month of Year")
        ax1.set_ylabel("Recorded Crash Count")
        ax1.set_xticks(x)
        ax1.set_xticklabels(m_stats["month_name"])
        ax1.legend(loc="upper left")

        ax2 = ax1.twinx()
        ax2.plot(x, m_stats["severity_rate"], color="#1b9e77", marker="D", linewidth=2.5, label="Severity Rate (%)")
        ax2.set_ylabel("Severity Rate (%)", color="#1b9e77")
        ax2.set_ylim(40, 85)
        ax2.tick_params(axis="y", labelcolor="#1b9e77")

        plt.title("Monthly Accident Distribution and Severity Rate in Chennai\nComparison of Total Incident Density vs. Severe Outcome Proportion", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_02_accident_distribution_month.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_03_accident_distribution_dow(self):
        """3. Accident distribution by day of week (Weekday vs Weekend)."""
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_stats = self.modeling_df.groupby("day_of_week").agg(
            total=("accident_id", "count"),
            severe=("severe_accident", "sum")
        ).reindex(dow_order).reset_index()
        dow_stats["severity_rate"] = dow_stats["severe"] / dow_stats["total"] * 100

        fig, ax = plt.subplots(figsize=(8, 4.5))
        sns.barplot(data=dow_stats, x="day_of_week", y="total", palette="Blues_d", ax=ax)
        ax.set_xlabel("Day of Week")
        ax.set_ylabel("Total Recorded Crashes")

        ax2 = ax.twinx()
        ax2.plot(range(len(dow_stats)), dow_stats["severity_rate"], color="#d62728", marker="o", linewidth=2.5, label="Severity Rate (%)")
        ax2.set_ylabel("Severity Rate (%)", color="#d62728")
        ax2.set_ylim(50, 80)
        ax2.tick_params(axis="y", labelcolor="#d62728")

        plt.title("Chennai Accident Occurrence & Severity by Day of Week\nHighlighting Weekend vs. Weekday Traffic Dynamics", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_03_accident_distribution_dow.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_04_accident_distribution_hour(self):
        """4. Accident distribution by hour of day (Diurnal traffic cycles)."""
        hr_stats = self.modeling_df.groupby("accident_hour").agg(
            total=("accident_id", "count"),
            severe=("severe_accident", "sum")
        ).reset_index()
        hr_stats["severity_rate"] = hr_stats["severe"] / hr_stats["total"] * 100

        fig, ax1 = plt.subplots(figsize=(10, 4.8))
        ax1.bar(hr_stats["accident_hour"], hr_stats["total"], color="#4575b4", alpha=0.85, width=0.7, label="Crash Count")
        ax1.set_xlabel("Hour of Day (00:00 to 23:00)")
        ax1.set_ylabel("Total Recorded Accidents", color="#4575b4")
        ax1.set_xticks(range(0, 24))

        # Highlight Peak Hours
        ax1.axvspan(8, 11, color="orange", alpha=0.15, label="Morning Peak (08:00-11:00)")
        ax1.axvspan(17, 21, color="red", alpha=0.15, label="Evening Peak (17:00-21:00)")

        ax2 = ax1.twinx()
        ax2.plot(hr_stats["accident_hour"], hr_stats["severity_rate"], color="#d73027", marker="s", linewidth=2.2, label="Severity Rate (%)")
        ax2.set_ylabel("Severity Rate (%)", color="#d73027")
        ax2.set_ylim(40, 90)
        ax2.tick_params(axis="y", labelcolor="#d73027")

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True)

        plt.title("Diurnal Hourly Accident Frequency and Severity Rate in Chennai\nContrasting Commuter Congestion Peak Volumes against Off-Peak Night Severity", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_04_accident_distribution_hour.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_05_severity_distribution(self):
        """5. Accident severity distribution (Categorical breakdown & Binary Target)."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

        # Multiclass original GCP categories
        counts = self.modeling_df["accident_severity"].value_counts()
        colors = ["#e41a1c", "#ff7f00", "#377eb8", "#4daf4a"]
        ax1.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=140, colors=colors, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
        ax1.set_title("Official GCP Severity Categories\n(2021 Recorded Total = 5,035)", fontsize=11)

        # Binary Target
        target_counts = self.modeling_df["severe_accident"].value_counts()
        labels = ["Severe (Fatal / Grievous)", "Non-Severe (Minor / None)"]
        ax2.bar(labels, target_counts, color=["#d62728", "#1f77b4"], width=0.55)
        for i, v in enumerate(target_counts):
            pct = v / len(self.modeling_df) * 100
            ax2.text(i, v + 70, f"{v:,} ({pct:.1f}%)", ha="center", fontweight="bold", fontsize=10)
        ax2.set_ylabel("Accident Count")
        ax2.set_ylim(0, max(target_counts) * 1.15)
        ax2.set_title("Binary Target (`severe_accident`)\n68.0% Severe vs. 32.0% Non-Severe", fontsize=11)

        plt.suptitle("Chennai Road Crash Severity Outcome Distribution", fontsize=13, y=1.02)
        fig.tight_layout()
        out = self.vis_dir / "eda_05_severity_distribution.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_06_vehicle_vs_severity(self):
        """6. Vehicle type versus severity."""
        v_stats = self.modeling_df.groupby("vehicle_type")["severe_accident"].agg(
            total="count",
            severe_count="sum",
            severity_rate="mean"
        ).reset_index()
        v_stats["severity_rate_pct"] = v_stats["severity_rate"] * 100
        v_stats = v_stats.sort_values("severity_rate_pct", ascending=True)

        fig, ax = plt.subplots(figsize=(9, 4.8))
        bars = ax.barh(v_stats["vehicle_type"], v_stats["severity_rate_pct"], color="#fc8d59", edgecolor="#d73027", height=0.6)
        ax.set_xlabel("Severity Rate (% Fatal or Grievous Injury)")
        ax.set_xlim(0, 100)
        ax.set_ylabel("Involved Vehicle Category")

        # Annotate bars with counts
        for bar, total, count, rate in zip(bars, v_stats["total"], v_stats["severe_count"], v_stats["severity_rate_pct"]):
            ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
                    f"{rate:.1f}% ({count:,} of {total:,})", va="center", fontsize=9, fontweight="bold")

        plt.title("Accident Severity Rate Across Vehicle Categories in Chennai\nVulnerability and Impact Severity of Heavy Commercial vs. Two-Wheeled Transport", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_06_vehicle_vs_severity.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_07_weather_vs_severity(self):
        """7. Weather & rainfall intensity versus severity."""
        w_stats = self.modeling_df.groupby("rainfall_category")["severe_accident"].agg(
            total="count",
            severity_rate="mean"
        ).reset_index()
        w_stats["severity_rate_pct"] = w_stats["severity_rate"] * 100
        w_order = ["No Rain", "Very Light", "Moderate Rain", "Heavy Rain"]
        w_stats = w_stats.set_index("rainfall_category").reindex(w_order).reset_index().dropna()

        fig, ax1 = plt.subplots(figsize=(8, 4.5))
        ax1.bar(w_stats["rainfall_category"], w_stats["total"], color="#91bfdb", width=0.5, label="Total Crashes")
        ax1.set_xlabel("Rainfall Intensity (NASA POWER Daily Precipitation)")
        ax1.set_ylabel("Crash Count", color="#4575b4")

        ax2 = ax1.twinx()
        ax2.plot(w_stats["rainfall_category"], w_stats["severity_rate_pct"], color="#d73027", marker="o", linewidth=2.5, label="Severity Rate (%)")
        ax2.set_ylabel("Severity Rate (%)", color="#d73027")
        ax2.set_ylim(50, 85)
        ax2.tick_params(axis="y", labelcolor="#d73027")

        plt.title("Chennai Accident Severity Under Varying Rainfall Intensities\nEvaluating Road Wetness and Hydroplaning Risk on Crash Severity", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_07_weather_vs_severity.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_08_lighting_vs_severity(self):
        """8. Lighting condition versus severity."""
        l_stats = self.modeling_df.groupby("lighting_condition")["severe_accident"].agg(
            total="count",
            severe="sum",
            severity_rate="mean"
        ).reset_index()
        l_stats["severity_rate_pct"] = l_stats["severity_rate"] * 100
        l_stats = l_stats.sort_values("severity_rate_pct", ascending=True)

        fig, ax = plt.subplots(figsize=(9, 4.2))
        bars = ax.barh(l_stats["lighting_condition"], l_stats["severity_rate_pct"], color="#67a9cf", edgecolor="#02818a", height=0.55)
        ax.set_xlabel("Severity Rate (% Fatal / Grievous Injury)")
        ax.set_xlim(0, 100)
        ax.set_ylabel("Ambient Lighting Condition")

        for bar, total, sev, rate in zip(bars, l_stats["total"], l_stats["severe"], l_stats["severity_rate_pct"]):
            ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
                    f"{rate:.1f}% ({sev:,} of {total:,})", va="center", fontsize=9, fontweight="bold")

        plt.title("Accident Severity Rate Across Ambient Lighting Conditions in Chennai\nImpact of Night Darkness & Inadequate Streetlighting on Fatal Outcomes", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_08_lighting_vs_severity.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_09_road_class_vs_severity(self):
        """9. Road classification and speed limits versus severity."""
        r_stats = self.modeling_df.groupby(["road_classification", "speed_limit_kmh"])["severe_accident"].agg(
            total="count",
            severity_rate="mean"
        ).reset_index()
        r_stats["severity_rate_pct"] = r_stats["severity_rate"] * 100
        r_stats = r_stats.sort_values("speed_limit_kmh")

        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        sns.barplot(data=r_stats, x="road_classification", y="severity_rate_pct", palette="Reds", ax=ax)
        ax.set_xlabel("Road Network Hierarchy")
        ax.set_ylabel("Severity Rate (%)")
        ax.set_ylim(0, 100)

        for i, row in r_stats.reset_index().iterrows():
            ax.text(i, row["severity_rate_pct"] + 2, f"{row['severity_rate_pct']:.1f}%\n({row['speed_limit_kmh']} km/h limit)", ha="center", fontsize=9)

        plt.title("Chennai Accident Severity Rate Across Road Classifications\nHigher Operating Speeds on Trunk/Expressways Elevating Injury Severity", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_09_road_class_vs_severity.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_10_junction_vs_severity(self):
        """10. Junction layout type versus severity."""
        j_stats = self.modeling_df.groupby("junction_type")["severe_accident"].agg(
            total="count",
            severe="sum",
            severity_rate="mean"
        ).reset_index()
        j_stats["severity_rate_pct"] = j_stats["severity_rate"] * 100
        j_stats = j_stats.sort_values("severity_rate_pct", ascending=True)

        fig, ax = plt.subplots(figsize=(9, 4.5))
        bars = ax.barh(j_stats["junction_type"], j_stats["severity_rate_pct"], color="#8073ac", edgecolor="#542788", height=0.55)
        ax.set_xlabel("Severity Rate (% Fatal / Grievous)")
        ax.set_xlim(0, 100)
        ax.set_ylabel("Junction / Geometric Design")

        for bar, total, sev, rate in zip(bars, j_stats["total"], j_stats["severe"], j_stats["severity_rate_pct"]):
            ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
                    f"{rate:.1f}% ({sev:,} / {total:,})", va="center", fontsize=9, fontweight="bold")

        plt.title("Accident Severity Rate Across Road Geometric & Junction Types\nComparing Grade-Separated Bridges, Roundabouts, and At-Grade Intersections", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_10_junction_vs_severity.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_11_geographical_density(self):
        """11. Geographical accident distribution across police stations/taluks."""
        top_stations = self.modeling_df["police_station"].value_counts().head(10).reset_index()
        top_stations.columns = ["police_station", "accident_count"]

        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=top_stations, y="police_station", x="accident_count", palette="viridis", ax=ax)
        ax.set_xlabel("Total Recorded Accident Incidents")
        ax.set_ylabel("Police Station Jurisdiction")

        for i, v in enumerate(top_stations["accident_count"]):
            ax.text(v + 5, i, f"{v:,}", va="center", fontsize=9, fontweight="bold")

        plt.title("Top 10 High-Concentration Traffic Police Jurisdictions in Chennai\nEmpirical Crash Density Concentration (Not Normalized for Traffic Volume)", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_11_geographical_density.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def plot_12_geographical_severity_ratio(self):
        """12. Accident severity ratio across geographic taluks."""
        t_stats = self.modeling_df.groupby("taluk")["severe_accident"].agg(
            total="count",
            severity_rate="mean"
        ).reset_index()
        t_stats["severity_rate_pct"] = t_stats["severity_rate"] * 100
        t_stats = t_stats.sort_values("severity_rate_pct", ascending=True)

        fig, ax = plt.subplots(figsize=(9, 4.8))
        bars = ax.barh(t_stats["taluk"], t_stats["severity_rate_pct"], color="#dfc27d", edgecolor="#a6611a", height=0.55)
        ax.set_xlabel("Severity Rate (% Fatal or Grievous Injury)")
        ax.set_xlim(0, 100)
        ax.set_ylabel("Administrative Taluk / Region")

        for bar, total, rate in zip(bars, t_stats["total"], t_stats["severity_rate_pct"]):
            ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
                    f"{rate:.1f}% (N={total})", va="center", fontsize=9, fontweight="bold")

        plt.title("Accident Severity Rate Across Chennai Administrative Taluks\nGeographic Disparity in Crash Outcomes Across Suburban vs. Core Urban Zones", pad=12)
        fig.tight_layout()
        out = self.vis_dir / "eda_12_geographical_severity_ratio.png"
        plt.savefig(out)
        plt.close()
        logger.info(f"Saved {out.name}")

    def generate_all_visualizations(self):
        logger.info("Generating all 12 publication-grade EDA visualizations...")
        self.plot_01_accident_trends_year()
        self.plot_02_accident_distribution_month()
        self.plot_03_accident_distribution_dow()
        self.plot_04_accident_distribution_hour()
        self.plot_05_severity_distribution()
        self.plot_06_vehicle_vs_severity()
        self.plot_07_weather_vs_severity()
        self.plot_08_lighting_vs_severity()
        self.plot_09_road_class_vs_severity()
        self.plot_10_junction_vs_severity()
        self.plot_11_geographical_density()
        self.plot_12_geographical_severity_ratio()
        logger.info("All 12 visualizations successfully generated and saved to results/visualizations/.")


if __name__ == "__main__":
    eda = ChennaiAccidentEDA()
    eda.generate_all_visualizations()

