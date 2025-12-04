"""
Explainable Boosting Machine for Skills Gap Prediction
Uses InterpretML for high-accuracy explainable predictions
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from interpret.glassbox import ExplainableBoostingClassifier
from interpret import show
import warnings
warnings.filterwarnings('ignore')


class SkillsGapEBM:
    """EBM classifier for predicting digital skills gap risk"""

    def __init__(self, data_path='../../data/skills_gap_navigator/data/integrated_dataset.csv'):
        self.data_path = Path(data_path)
        self.model = None
        self.feature_names = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.countries_test = None
        self.explainer = None

    def load_and_prepare_data(self, target_col='risk_level'):
        """Load integrated data and prepare for modeling"""
        print("Loading integrated dataset...")
        df = pd.read_csv(self.data_path)

        # Store country names for later reference
        self.country_names = df['country'].values

        # Separate features from target
        exclude_cols = ['country', 'year', 'risk_score', 'risk_category', 'risk_level',
                       'income_group', 'region']
        self.feature_names = [c for c in df.columns if c not in exclude_cols]

        # Handle categorical variables if present
        X = df[self.feature_names].copy()

        # Fill missing values with median for numeric columns
        for col in X.columns:
            if X[col].dtype in [np.float64, np.int64]:
                X[col] = X[col].fillna(X[col].median())

        y = df[target_col]

        # Train-test split (stratified by risk level)
        indices = np.arange(len(X))
        X_train_idx, X_test_idx = train_test_split(
            indices,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        self.X_train = X.iloc[X_train_idx]
        self.X_test = X.iloc[X_test_idx]
        self.y_train = y.iloc[X_train_idx]
        self.y_test = y.iloc[X_test_idx]
        self.countries_test = df.iloc[X_test_idx]['country'].values

        print(f"\n✓ Data prepared:")
        print(f"  Features: {len(self.feature_names)}")
        print(f"  Training samples: {len(self.X_train)}")
        print(f"  Test samples: {len(self.X_test)}")
        print(f"  Class distribution: {dict(y.value_counts())}")

        return self

    def train_model(self, interactions=10):
        """Train EBM classifier"""
        print("\n" + "="*80)
        print("TRAINING EXPLAINABLE BOOSTING MACHINE")
        print("="*80)

        # Initialize EBM with optimal parameters
        self.model = ExplainableBoostingClassifier(
            feature_names=self.feature_names,
            max_rounds=5000,
            learning_rate=0.01,
            interactions=interactions,
            max_leaves=3,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )

        print("Training model...")
        self.model.fit(self.X_train, self.y_train)

        print("✓ Model trained successfully")

        return self

    def evaluate_model(self):
        """Evaluate model performance"""
        print("\n" + "="*80)
        print("MODEL EVALUATION")
        print("="*80)

        # Predictions
        y_pred = self.model.predict(self.X_test)
        y_pred_proba = self.model.predict_proba(self.X_test)

        # Accuracy metrics
        print("\nClassification Report:")
        unique_classes = sorted(self.y_test.unique())
        class_names = ['Ready', 'Emerging', 'High', 'Critical']
        target_names = [class_names[i] for i in unique_classes]
        print(classification_report(
            self.y_test,
            y_pred,
            labels=unique_classes,
            target_names=target_names
        ))

        # AUC (multiclass)
        try:
            auc = roc_auc_score(
                self.y_test,
                y_pred_proba,
                multi_class='ovr',
                average='weighted'
            )
            print(f"\n✓ Weighted AUC: {auc:.4f}")

            if auc >= 0.85:
                print("  🎯 TARGET MET: AUC > 0.85")
            else:
                print(f"  ⚠ Warning: AUC below target (need {0.85 - auc:.4f} improvement)")

        except Exception as e:
            print(f"Could not calculate AUC: {e}")

        # Confusion matrix
        print("\nConfusion Matrix:")
        cm = confusion_matrix(self.y_test, y_pred)
        print(cm)

        return auc if 'auc' in locals() else None

    def get_global_feature_importance(self):
        """Extract global feature importance for visualization"""
        print("\nExtracting feature importance...")

        # Get global explanation
        ebm_global = self.model.explain_global()

        # Extract importance scores
        importance_data = []
        for idx, feature_name in enumerate(ebm_global.data()['names']):
            importance = ebm_global.data()['scores'][idx]
            importance_data.append({
                'feature': feature_name,
                'importance': float(importance)
            })

        importance_df = pd.DataFrame(importance_data)
        importance_df = importance_df.sort_values('importance', ascending=False)

        print(f"✓ Top 10 most important features:")
        for i, row in importance_df.head(10).iterrows():
            print(f"  {row['feature']}: {row['importance']:.4f}")

        return importance_df

    def get_local_explanation(self, country_name=None, country_idx=None):
        """Get local explanation (waterfall) for a specific country"""
        if country_idx is None and country_name is not None:
            # Find country in test set
            country_indices = np.where(self.countries_test == country_name)[0]
            if len(country_indices) == 0:
                raise ValueError(f"Country '{country_name}' not in test set")
            country_idx = country_indices[0]

        if country_idx is None:
            raise ValueError("Must provide either country_name or country_idx")

        # Get local explanation
        ebm_local = self.model.explain_local(
            self.X_test.iloc[[country_idx]],
            self.y_test.iloc[[country_idx]]
        )

        # Extract waterfall data
        waterfall_data = {
            'country': self.countries_test[country_idx],
            'prediction': int(self.model.predict(self.X_test.iloc[[country_idx]])[0]),
            'prediction_proba': self.model.predict_proba(self.X_test.iloc[[country_idx]])[0].tolist(),
            'actual': int(self.y_test.iloc[country_idx]),
            'features': [],
            'intercept': float(ebm_local.data(0)['scores'][0])  # Base rate
        }

        # Extract feature contributions
        names = ebm_local.data(0)['names']
        scores = ebm_local.data(0)['scores']

        for i, (name, score) in enumerate(zip(names, scores)):
            if i == 0:  # Skip intercept
                continue
            waterfall_data['features'].append({
                'name': name,
                'contribution': float(score),
                'value': float(self.X_test.iloc[country_idx][name]) if name in self.X_test.columns else None
            })

        # Sort by absolute contribution
        waterfall_data['features'].sort(key=lambda x: abs(x['contribution']), reverse=True)

        return waterfall_data

    def get_shape_functions(self, top_n=10):
        """Extract shape functions (marginal effect curves) for top features"""
        print("\nExtracting shape functions...")

        ebm_global = self.model.explain_global()
        importance_df = self.get_global_feature_importance()
        top_features = importance_df.head(top_n)['feature'].tolist()

        shape_data = {}

        for feature in top_features:
            if feature in ebm_global.data()['names']:
                idx = list(ebm_global.data()['names']).index(feature)

                # Get the feature's data
                feature_data = ebm_global.data(idx)

                if 'left_names' in feature_data:  # Interaction term
                    continue

                # Handle different data formats
                if isinstance(feature_data, dict):
                    if 'names' in feature_data:
                        feat_vals = feature_data['names'] if isinstance(feature_data['names'], list) else feature_data['names'].tolist()
                    else:
                        feat_vals = list(range(len(feature_data['scores'])))

                    scores = feature_data['scores'] if isinstance(feature_data['scores'], list) else feature_data['scores'].tolist()

                    shape_data[feature] = {
                        'feature_values': feat_vals,
                        'scores': scores,
                        'type': feature_data.get('type', 'continuous')
                    }
                else:
                    # Skip if data format is unexpected
                    continue

        print(f"✓ Extracted shape functions for {len(shape_data)} features")

        return shape_data

    def export_model_artifacts(self, output_dir='../visualizations/data'):
        """Export all model artifacts for visualization"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print("\n" + "="*80)
        print("EXPORTING MODEL ARTIFACTS")
        print("="*80)

        # 1. Feature importance
        importance_df = self.get_global_feature_importance()
        importance_df.to_json(
            output_path / 'feature_importance.json',
            orient='records'
        )
        print(f"✓ Feature importance → {output_path / 'feature_importance.json'}")

        # 2. Shape functions
        shape_data = self.get_shape_functions(top_n=15)
        with open(output_path / 'shape_functions.json', 'w') as f:
            json.dump(shape_data, f, indent=2)
        print(f"✓ Shape functions → {output_path / 'shape_functions.json'}")

        # 3. All countries' predictions and explanations
        all_predictions = []
        for idx in range(len(self.X_test)):
            country = self.countries_test[idx]
            try:
                waterfall = self.get_local_explanation(country_idx=idx)
                all_predictions.append(waterfall)
            except Exception as e:
                print(f"Warning: Could not get explanation for {country}: {e}")

        with open(output_path / 'country_predictions.json', 'w') as f:
            json.dump(all_predictions, f, indent=2)
        print(f"✓ Country predictions → {output_path / 'country_predictions.json'}")

        # 4. Model metadata
        metadata = {
            'model_type': 'ExplainableBoostingClassifier',
            'n_features': len(self.feature_names),
            'feature_names': self.feature_names,
            'n_train_samples': len(self.X_train),
            'n_test_samples': len(self.X_test),
            'risk_categories': ['Ready', 'Emerging', 'High', 'Critical']
        }

        with open(output_path / 'model_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Model metadata → {output_path / 'model_metadata.json'}")

        print("\n✓ All artifacts exported successfully!")

        return output_path


if __name__ == '__main__':
    print("="*80)
    print("GLOBAL DIGITAL SKILLS GAP NAVIGATOR - EBM MODEL")
    print("="*80)

    # Initialize and train
    ebm = SkillsGapEBM()
    ebm.load_and_prepare_data()
    ebm.train_model(interactions=10)

    # Evaluate
    auc = ebm.evaluate_model()

    # Get explanations
    importance = ebm.get_global_feature_importance()

    # Export for visualization
    ebm.export_model_artifacts()

    print("\n" + "="*80)
    print("✓ MODEL TRAINING COMPLETE")
    print("="*80)
