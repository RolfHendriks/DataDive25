"""
Global Digital Skills Gap Navigator - Data Integration Pipeline
Integrates HAI, World Bank, and creates features for EBM model
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class SkillsGapDataIntegrator:
    """Integrates multiple data sources for skills gap analysis"""

    def __init__(self, base_path='../../data/POC'):
        self.base_path = Path(base_path)
        self.hai_data = None
        self.world_bank_data = None
        self.integrated_data = None

    def load_hai_data(self):
        """Load Stanford HAI database"""
        print("Loading HAI database...")
        hai_path = self.base_path / 'hai_full_database.csv'
        self.hai_data = pd.read_csv(hai_path)
        print(f"Loaded {len(self.hai_data)} records from {self.hai_data['PublishYear'].nunique()} years")
        print(f"Countries: {self.hai_data['CountryName'].nunique()}")
        return self

    def load_world_bank_data(self):
        """Load World Bank I2D2 data"""
        print("\nLoading World Bank data...")
        wb_path = self.base_path / 'Country Data Set.xlsx'
        self.world_bank_data = pd.read_excel(wb_path)
        print(f"Loaded {len(self.world_bank_data)} records")
        return self

    def create_ai_job_features(self, df):
        """Create AI job market features from HAI data"""
        features = pd.DataFrame()
        features['country'] = df['CountryName']
        features['year'] = df['PublishYear']

        # AI Talent & Skills
        features['ai_skills_penetration'] = df['relative_ai_skills_penetration']
        features['ai_hiring_rate'] = df['relative_ai_hiring_rate_yoy_ratio']
        features['ai_talent_concentration'] = df['ai_talent_concentration']
        features['ai_job_postings_pct'] = df['ai_job_postings_perc_of_all_job_postings']
        features['ai_talent_migration'] = df['net_migration_flow_ai_skills_per_10k']
        features['ai_gender_equality'] = df['ai_talent_concentration_gender_equality_index']

        # Research & Innovation
        features['ai_publications'] = df['number_of_total_publications']
        features['ai_citations'] = df['number_of_total_citations']
        features['ai_patents'] = df['number_of_total_patent_grants']
        features['ml_models'] = df['number_of_notable_ml_models']
        features['github_repos'] = df['number_of_github_repos']

        # Investment & Infrastructure
        features['private_investment'] = df['private_investment']
        features['newly_funded_companies'] = df['number_of_newly_funded_companies']
        features['internet_speed'] = df['internet_speed_median_download_mbps']
        features['supercomputers'] = df['number_of_supercomputers']

        # Policy & Awareness
        features['ai_bills_passed'] = df['num_ai_related_bills_passed']
        features['ai_policy_momentum'] = df['num_ai_related_bills_passed_3y_moving_average']
        features['has_ai_strategy'] = df['national_ai_strategy_is_released']

        # Demographics & Economy
        features['population'] = df['Population']
        features['income_group'] = df['IncomeGroup']
        features['region'] = df['Region']

        return features

    def create_labor_features(self, df):
        """Create labor market features from World Bank data"""
        features = pd.DataFrame()

        # Key columns (adjust based on actual World Bank data structure)
        if 'countryname' in df.columns:
            features['country'] = df['countryname']

        # Education levels (proxy for adaptability)
        edu_cols = [c for c in df.columns if 'education' in c.lower() or 'post secondary' in c.lower()]
        if edu_cols:
            features['higher_ed_pct'] = df[edu_cols].mean(axis=1)

        # Sector composition (vulnerability to automation)
        sector_cols = [c for c in df.columns if any(x in c.lower() for x in
                      ['agriculture', 'industry', 'manufacturing', 'service', 'commerce'])]
        for col in sector_cols[:10]:  # Limit to prevent too many features
            clean_name = col.lower().replace(' ', '_').replace(',', '')[:30]
            features[clean_name] = df[col]

        # Employment formality
        if 'Share of informal jobs, aged 15-64' in df.columns:
            features['informal_employment_pct'] = df['Share of informal jobs, aged 15-64']

        # Occupation types
        occupation_cols = [c for c in df.columns if 'occupation' in c.lower() or
                          any(x in c.lower() for x in ['professional', 'clerk', 'technician', 'operator'])]
        for col in occupation_cols[:8]:
            clean_name = col.lower().replace(' ', '_').replace(',', '')[:30]
            features[clean_name] = df[col]

        return features

    def engineer_job_velocity_features(self, df):
        """Calculate job posting velocity and trend features"""
        df = df.sort_values(['country', 'year'])

        # Year-over-year changes
        for col in ['ai_job_postings_pct', 'ai_skills_penetration', 'ai_hiring_rate']:
            if col in df.columns:
                df[f'{col}_growth'] = df.groupby('country')[col].pct_change()
                df[f'{col}_acceleration'] = df.groupby('country')[f'{col}_growth'].diff()

        # 3-year trends
        for col in ['ai_job_postings_pct', 'ai_publications', 'private_investment']:
            if col in df.columns:
                df[f'{col}_trend_3y'] = df.groupby('country')[col].transform(
                    lambda x: x.rolling(3, min_periods=1).mean()
                )

        return df

    def create_risk_target(self, df, target_year=2027):
        """
        Create target variable: Critical Skills Mismatch by 2027
        Categories: Ready (0), Emerging (1), High (2), Critical (3)
        """
        # Use latest available data to project risk
        latest = df.groupby('country').tail(1).copy()

        risk_score = 0

        # Factor 1: Low AI job postings but high automation potential (mismatch)
        if 'ai_job_postings_pct' in latest.columns:
            risk_score += (1 - latest['ai_job_postings_pct'].fillna(0) /
                          latest['ai_job_postings_pct'].max()) * 25

        # Factor 2: Low skills penetration
        if 'ai_skills_penetration' in latest.columns:
            risk_score += (1 - latest['ai_skills_penetration'].fillna(0) /
                          latest['ai_skills_penetration'].max()) * 20

        # Factor 3: Negative hiring trends
        if 'ai_hiring_rate' in latest.columns:
            risk_score += (1 - latest['ai_hiring_rate'].fillna(1)) * 15

        # Factor 4: Low education/research capacity
        if 'ai_publications' in latest.columns:
            pub_norm = latest['ai_publications'].fillna(0) / latest['population']
            risk_score += (1 - pub_norm / pub_norm.max()) * 15

        # Factor 5: Infrastructure gaps
        if 'internet_speed' in latest.columns:
            risk_score += (1 - latest['internet_speed'].fillna(0) /
                          latest['internet_speed'].max()) * 15

        # Factor 6: No AI policy
        if 'has_ai_strategy' in latest.columns:
            risk_score += (1 - latest['has_ai_strategy'].fillna(0)) * 10

        # Classify into 4 categories
        latest['risk_score'] = risk_score
        latest['risk_category'] = pd.cut(
            risk_score,
            bins=[-1, 25, 50, 75, 100],
            labels=['Ready', 'Emerging', 'High', 'Critical']
        )
        latest['risk_level'] = pd.cut(
            risk_score,
            bins=[-1, 25, 50, 75, 100],
            labels=[0, 1, 2, 3]
        ).astype(int)

        return latest[['country', 'risk_score', 'risk_category', 'risk_level']]

    def integrate_and_prepare(self):
        """Main integration pipeline"""
        print("\n" + "="*80)
        print("GLOBAL DIGITAL SKILLS GAP NAVIGATOR - DATA INTEGRATION")
        print("="*80)

        # Load data
        self.load_hai_data()

        # Create AI features
        print("\nEngineering AI job market features...")
        ai_features = self.create_ai_job_features(self.hai_data)

        # Add velocity features
        print("Calculating job posting velocity and trends...")
        ai_features = self.engineer_job_velocity_features(ai_features)

        # Create target variable
        print("Creating risk target variable...")
        risk_targets = self.create_risk_target(ai_features)

        # Get most recent year for each country for modeling
        latest_features = ai_features.groupby('country').tail(1).copy()

        # Merge with targets
        self.integrated_data = latest_features.merge(
            risk_targets[['country', 'risk_score', 'risk_category', 'risk_level']],
            on='country',
            how='left'
        )

        # Save integrated dataset
        output_path = self.base_path.parent / 'skills_gap_navigator' / 'data' / 'integrated_dataset.csv'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.integrated_data.to_csv(output_path, index=False)

        print(f"\n✓ Integrated dataset created: {len(self.integrated_data)} countries")
        print(f"✓ Features: {len(self.integrated_data.columns)} columns")
        print(f"✓ Saved to: {output_path}")

        # Print risk distribution
        print("\nRisk Category Distribution:")
        print(self.integrated_data['risk_category'].value_counts().sort_index())

        # Print feature summary
        print("\nTop 10 Features (by non-null count):")
        feature_counts = self.integrated_data.notna().sum().sort_values(ascending=False)
        print(feature_counts.head(10))

        return self.integrated_data

    def get_feature_list(self):
        """Get list of features for modeling"""
        if self.integrated_data is None:
            raise ValueError("Must run integrate_and_prepare() first")

        exclude_cols = ['country', 'year', 'risk_score', 'risk_category', 'risk_level',
                       'income_group', 'region']
        feature_cols = [c for c in self.integrated_data.columns if c not in exclude_cols]

        return feature_cols


if __name__ == '__main__':
    # Run integration pipeline
    integrator = SkillsGapDataIntegrator()
    integrated_df = integrator.integrate_and_prepare()

    print("\n" + "="*80)
    print("SAMPLE DATA (first 3 countries):")
    print("="*80)
    print(integrated_df[['country', 'risk_category', 'risk_score',
                        'ai_skills_penetration', 'ai_job_postings_pct']].head(3))

    print("\n✓ Data integration complete!")
