import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

class SampleDataGenerator:
    def __init__(self):
        """Initialize sample data generator"""
        self.product_ids = [f"P{str(i).zfill(3)}" for i in range(1, 101)]  # P001 to P100
        self.product_names = [
            f"Product {i}" for i in range(1, 101)
        ]
        self.categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty', 'Toys', 'Food']
        self.brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE', 'BrandF', 'BrandG', 'BrandH']
        
    def generate_sample_files(self):
        """Generate all sample data files"""
        # Create sample_data directory
        os.makedirs('sample_data', exist_ok=True)
        
        # Generate each dataset
        self._generate_ad_sales_data()
        self._generate_total_sales_data()
        self._generate_eligibility_data()
        
        print("Sample data files generated successfully!")
    
    def _generate_ad_sales_data(self):
        """Generate Product-Level Ad Sales and Metrics data"""
        data = []
        
        for product_id in self.product_ids:
            # Generate realistic ad metrics
            ad_spend = round(random.uniform(100, 5000), 2)
            clicks = random.randint(50, 2000)
            impressions = random.randint(clicks * 10, clicks * 50)
            conversions = random.randint(1, clicks // 10 if clicks >= 10 else 1)
            
            cpc = round(ad_spend / clicks if clicks > 0 else 0, 2)
            cpm = round((ad_spend / impressions) * 1000 if impressions > 0 else 0, 2)
            ctr = round((clicks / impressions) * 100 if impressions > 0 else 0, 2)
            conversion_rate = round((conversions / clicks) * 100 if clicks > 0 else 0, 2)
            
            # Ad revenue should be higher than ad spend for profitable campaigns
            ad_revenue = round(ad_spend * random.uniform(0.5, 3.0), 2)
            
            data.append({
                'product_id': product_id,
                'ad_spend': ad_spend,
                'ad_revenue': ad_revenue,
                'clicks': clicks,
                'impressions': impressions,
                'conversions': conversions,
                'cpc': cpc,
                'cpm': cpm,
                'ctr': ctr,
                'conversion_rate': conversion_rate
            })
        
        df = pd.DataFrame(data)
        df.to_csv('sample_data/ad_sales_metrics.csv', index=False)
        print(f"Generated ad_sales_metrics.csv with {len(df)} records")
    
    def _generate_total_sales_data(self):
        """Generate Product-Level Total Sales and Metrics data"""
        data = []
        
        for product_id in self.product_ids:
            # Generate realistic sales metrics
            units_sold = random.randint(10, 1000)
            avg_order_value = round(random.uniform(20, 500), 2)
            total_revenue = round(units_sold * avg_order_value, 2)
            
            # Total sales might be slightly different from revenue due to returns/discounts
            total_sales = round(total_revenue * random.uniform(0.85, 1.0), 2)
            
            profit_margin = round(random.uniform(10, 60), 2)  # Percentage
            
            data.append({
                'product_id': product_id,
                'total_revenue': total_revenue,
                'total_sales': total_sales,
                'units_sold': units_sold,
                'avg_order_value': avg_order_value,
                'profit_margin': profit_margin
            })
        
        df = pd.DataFrame(data)
        df.to_csv('sample_data/total_sales_metrics.csv', index=False)
        print(f"Generated total_sales_metrics.csv with {len(df)} records")
    
    def _generate_eligibility_data(self):
        """Generate Product-Level Eligibility Table data"""
        data = []
        
        for i, product_id in enumerate(self.product_ids):
            product_name = self.product_names[i]
            category = random.choice(self.categories)
            brand = random.choice(self.brands)
            
            # 80% of products are eligible for ads
            eligible_for_ads = random.choices([True, False], weights=[0.8, 0.2])[0]
            
            if eligible_for_ads:
                eligibility_reason = 'Approved'
            else:
                eligibility_reason = random.choice([
                    'Policy Violation',
                    'Low Quality Score',
                    'Restricted Category',
                    'Pending Review'
                ])
            
            data.append({
                'product_id': product_id,
                'product_name': product_name,
                'category': category,
                'brand': brand,
                'eligible_for_ads': eligible_for_ads,
                'eligibility_reason': eligibility_reason
            })
        
        df = pd.DataFrame(data)
        df.to_csv('sample_data/eligibility_table.csv', index=False)
        print(f"Generated eligibility_table.csv with {len(df)} records")
    
    def generate_time_series_data(self, days=30):
        """Generate time-series data for trend analysis"""
        dates = [datetime.now() - timedelta(days=x) for x in range(days)]
        dates.reverse()
        
        data = []
        for date in dates:
            daily_sales = random.randint(1000, 10000)
            daily_ad_spend = random.randint(100, 1000)
            daily_revenue = random.randint(1200, 12000)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'daily_sales': daily_sales,
                'daily_ad_spend': daily_ad_spend,
                'daily_revenue': daily_revenue
            })
        
        df = pd.DataFrame(data)
        df.to_csv('sample_data/daily_metrics.csv', index=False)
        print(f"Generated daily_metrics.csv with {len(df)} records")
