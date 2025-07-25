#!/usr/bin/env python3
"""
Custom Report Generator for Cleaned CPT Data - USER-FRIENDLY VERSION WITH PREVIEW
Generates a comprehensive PDF report with easy-to-understand charts and explanations
Includes preview functionality to see report before download
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from io import BytesIO
import streamlit as st

# ReportLab imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_custom_cpt_report(csv_file_path):
    """Generate a user-friendly PDF report from cleaned CPT data"""
    
    # Read the CSV data
    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")
        return None
    
    # Create BytesIO object to store the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Add title
    cpt_code = df['billing_code'].iloc[0] if 'billing_code' in df.columns else "27130"
    elements.append(Paragraph(f"CPT {cpt_code} Analysis Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Add report metadata
    metadata_style = ParagraphStyle(
        'Metadata',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray
    )
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", metadata_style))
    elements.append(Paragraph(f"Insurance: EMPLOYER", metadata_style))
    elements.append(Paragraph(f"Plan: 360-orthopedics", metadata_style))
    elements.append(Paragraph(f"CPT Code: {cpt_code}", metadata_style))
    elements.append(Paragraph(f"Total Records: {len(df):,}", metadata_style))
    elements.append(Spacer(1, 20))
    
    # =================================================================
    # RATE STATISTICS AND ANALYSIS - IMPROVED FOR USER-FRIENDLINESS
    # =================================================================
    
    elements.append(Paragraph("Rate Analysis - What Do Providers Charge?", styles['Heading2']))
    elements.append(Spacer(1, 12))
    
    # Add explanation paragraph for non-technical users
    explanation_style = ParagraphStyle(
        'Explanation',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=12
    )
    elements.append(Paragraph(
        "This section shows how much different healthcare providers charge for this procedure. "
        "The table below shows key statistics, and the chart shows the distribution of rates across all providers.",
        explanation_style
    ))
    
    if 'negotiated_rate' in df.columns:
        rates = df['negotiated_rate'].dropna()
        if len(rates) > 0:
            # Basic statistics with user-friendly descriptions
            rate_stats = [
                ["What This Means", "Value"],
                ["Average Rate", f"${rates.mean():.2f}"],
                ["Most Common Rate (Median)", f"${rates.median():.2f}"],
                ["Lowest Rate Found", f"${rates.min():.2f}"],
                ["Highest Rate Found", f"${rates.max():.2f}"],
                ["Range (High - Low)", f"${rates.max() - rates.min():.2f}"],
                ["Total Providers Analyzed", f"{len(rates):,}"]
            ]
            
            # Add percentiles with better descriptions
            percentiles = [25, 50, 75, 90, 95]
            rate_percentiles = rates.quantile(q=[p/100 for p in percentiles])
            percentile_descriptions = {
                25: "25% of providers charge less than",
                50: "50% of providers charge less than", 
                75: "75% of providers charge less than",
                90: "90% of providers charge less than",
                95: "95% of providers charge less than"
            }
            
            for p, value in zip(percentiles, rate_percentiles):
                rate_stats.append([percentile_descriptions[p], f"${value:.2f}"])
            
            rate_table = Table(rate_stats, colWidths=[200, 100])
            rate_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(rate_table)
            elements.append(Spacer(1, 20))
            
            # Generate IMPROVED rate distribution plot
            plt.figure(figsize=(12, 6))
            
            # Create the histogram with better styling
            n, bins, patches = plt.hist(rates, bins=25, alpha=0.7, color='skyblue', edgecolor='navy', linewidth=1.5)
            
            # Improve title and labels for non-technical users
            plt.title(f'How Much Do Providers Charge for CPT {cpt_code}?\n'
                     f'Distribution of Rates Across {len(rates):,} Healthcare Providers', 
                     fontsize=12, fontweight='bold', pad=15)
            plt.xlabel('Cost in US Dollars', fontsize=12, fontweight='bold')
            plt.ylabel('Number of Providers', fontsize=12, fontweight='bold')
            
            # Format x-axis to show dollar signs and better spacing
            ax = plt.gca()
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # Add grid for easier reading
            plt.grid(True, alpha=0.3, linestyle='--', color='gray')
            
            # Add summary statistics as text on the chart
            mean_rate = rates.mean()
            median_rate = rates.median()
            min_rate = rates.min()
            max_rate = rates.max()
            
            stats_text = (f'Quick Stats:\n'
                         f'Average: ${mean_rate:,.0f}\n'
                         f'Most Common: ${median_rate:,.0f}\n'
                         f'Range: ${min_rate:,.0f} - ${max_rate:,.0f}\n'
                         f'Total Providers: {len(rates):,}')
            
            plt.text(0.98, 0.98, stats_text, 
                    transform=ax.transAxes, fontsize=12, 
                    verticalalignment='top', horizontalalignment='right',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, 
                             edgecolor='darkblue', linewidth=2))
            
            # Set reasonable axis limits to focus on the main data (remove extreme outliers)
            plt.xlim(rates.min() * 0.95, rates.quantile(0.95) * 1.05)
            
            # Improve layout
            plt.tight_layout()
            
            # Save plot to BytesIO
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=300, facecolor='white')
            plt.close()
            
            # Add plot to PDF
            img = Image(img_buffer)
            img.drawHeight = 5*inch
            img.drawWidth = 8*inch
            elements.append(img)
            elements.append(Spacer(1, 20))
    
    # =================================================================
    # BILLING CLASS ANALYSIS - IMPROVED
    # =================================================================
    
    if 'billing_class' in df.columns:
        elements.append(Paragraph("Billing Class Analysis", styles['Heading2']))
        
        billing_counts = df['billing_class'].value_counts()
        
        billing_data = [["Service Type", "Number of Providers", "Percentage"]]
        total_billing = len(df)
        for class_name, count in billing_counts.items():
            percentage = (count / total_billing) * 100
            billing_data.append([class_name, str(count), f"{percentage:.1f}%"])
        
        billing_table = Table(billing_data, colWidths=[150, 120, 100])
        billing_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(billing_table)
        elements.append(Spacer(1, 12))
        
        # Add billing class rate analysis if rates are available
        if 'negotiated_rate' in df.columns:
            billing_rates = df.groupby('billing_class')['negotiated_rate'].agg(['mean', 'median', 'std', 'count']).round(2)
            
            billing_rate_data = [["Service Type", "Average Rate", "Most Common Rate", "Rate Variation", "Count"]]
            for class_name, stats in billing_rates.iterrows():
                billing_rate_data.append([
                    class_name,
                    f"${stats['mean']:.2f}",
                    f"${stats['median']:.2f}",
                    f"${stats['std']:.2f}",
                    str(int(stats['count']))
                ])
            
            billing_rate_table = Table(billing_rate_data, colWidths=[100, 80, 100, 80, 60])
            billing_rate_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(billing_rate_table)
            elements.append(Spacer(1, 20))
    
    # =================================================================
    # NEGOTIATED TYPE ANALYSIS - IMPROVED
    # =================================================================
    
    if 'negotiated_type' in df.columns:
        elements.append(Paragraph("Contract Type Analysis - Payment Methods", styles['Heading2']))
        
        # Add explanation
        elements.append(Paragraph(
            "This shows different types of payment contracts between insurance companies and healthcare providers. "
            "Different contract types can affect the final cost you pay.",
            explanation_style
        ))
        
        neg_type_counts = df['negotiated_type'].value_counts()
        
        neg_type_data = [["Contract Type", "Number of Providers", "Percentage"]]
        total_neg = len(df)
        for neg_type, count in neg_type_counts.items():
            percentage = (count / total_neg) * 100
            neg_type_data.append([neg_type, str(count), f"{percentage:.1f}%"])
        
        neg_type_table = Table(neg_type_data, colWidths=[150, 120, 100])
        neg_type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(neg_type_table)
        elements.append(Spacer(1, 20))
    
    # =================================================================
    # COMPLETE GEOGRAPHIC DISTRIBUTION (ALL CITIES) - IMPROVED
    # =================================================================
    
    if 'city' in df.columns:
        elements.append(Paragraph("Geographic Distribution - Where Are Providers Located?", styles['Heading2']))
        
        # Add explanation
        elements.append(Paragraph(
            "This section shows which cities have healthcare providers offering this procedure and their average rates. "
            "This can help you find providers in your area or compare costs across different locations.",
            explanation_style
        ))
        
        elements.append(Paragraph("All Cities with Providers", styles['Heading3']))
        
        city_stats = df['city'].value_counts().sort_values(ascending=False)
        
        # Create comprehensive city data - ALL cities, not just top 10
        city_data = [["City", "# of Providers", "% of Total", "Average Rate", "Most Common Rate"]]
        total_providers = len(df)
        
        for city, count in city_stats.items():
            percentage = (count / total_providers) * 100
            city_df = df[df['city'] == city]
            
            if 'negotiated_rate' in df.columns:
                avg_rate = city_df['negotiated_rate'].mean()
                median_rate = city_df['negotiated_rate'].median()
                city_data.append([
                    city[:20] + "..." if len(city) > 20 else city,  # Truncate long city names
                    str(count),
                    f"{percentage:.1f}%",
                    f"${avg_rate:.0f}",
                    f"${median_rate:.0f}"
                ])
            else:
                city_data.append([
                    city[:20] + "..." if len(city) > 20 else city,
                    str(count),
                    f"{percentage:.1f}%",
                    "N/A",
                    "N/A"
                ])
        
        # Create table with appropriate column widths
        city_table = Table(city_data, colWidths=[120, 70, 60, 80, 90])
        city_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.moccasin),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(city_table)
        elements.append(Spacer(1, 12))
        
        # Add geographic summary
        total_cities = len(city_stats)
        elements.append(Paragraph(f"Total Unique Cities: {total_cities}", styles['Normal']))
        elements.append(Paragraph(f"City with Most Providers: {city_stats.index[0]} ({city_stats.iloc[0]} providers)", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Create Average Negotiated Rate by City chart
        plt.figure(figsize=(12, 6))
        
        # Calculate average rates by city for top 15 cities (by provider count)
        top_15_cities = city_stats.head(15)
        city_avg_rates = []
        city_names = []
        
        for city in top_15_cities.index:
            city_df = df[df['city'] == city]
            if 'negotiated_rate' in df.columns and len(city_df) > 0:
                avg_rate = city_df['negotiated_rate'].mean()
                city_avg_rates.append(avg_rate)
                city_names.append(city)
        
        bars = plt.bar(range(len(city_names)), city_avg_rates, 
                      color='gold', edgecolor='darkorange', linewidth=2)
        
        plt.title(f'Average Negotiated Rate for CPT {cpt_code} by City\nTop 15 Cities by Provider Count', 
                 fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Cities', fontsize=12, fontweight='bold')
        plt.ylabel('Average Negotiated Rate ($)', fontsize=12, fontweight='bold')
        plt.xticks(range(len(city_names)), city_names, rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # Format y-axis to show dollar signs
        ax = plt.gca()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'${height:,.0f}', ha='center', va='bottom', 
                    fontsize=9, fontweight='bold')
        
        # Improve styling
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.tight_layout()
        
        # Save plot to BytesIO
        geo_img_buffer = BytesIO()
        plt.savefig(geo_img_buffer, format='png', bbox_inches='tight', dpi=300, facecolor='white')
        plt.close()
        
        # Add plot to PDF
        geo_img = Image(geo_img_buffer)
        geo_img.drawHeight = 4*inch
        geo_img.drawWidth = 7*inch
        elements.append(geo_img)
        elements.append(Spacer(1, 20))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def show_report_preview(csv_file_path):
    """Show a preview of what will be in the PDF report"""
    
    # Read the CSV data
    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")
        return None
    
    cpt_code = df['billing_code'].iloc[0] if 'billing_code' in df.columns else "27130"
    
    st.markdown("---")
    st.markdown(f"# 📋 Report Preview - CPT {cpt_code}")
    st.markdown(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown(f"**Total Records:** {len(df):,}")
    
    # Rate Analysis Preview
    st.markdown("## 💰 Rate Analysis")
    st.markdown("This section shows how much different healthcare providers charge for this procedure.")
    
    if 'negotiated_rate' in df.columns:
        rates = df['negotiated_rate'].dropna()
        if len(rates) > 0:
            
            # Create two columns for stats and chart
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### 📊 Key Statistics")
                st.metric("Average Rate", f"${rates.mean():.2f}")
                st.metric("Most Common Rate", f"${rates.median():.2f}")
                st.metric("Lowest Rate", f"${rates.min():.2f}")
                st.metric("Highest Rate", f"${rates.max():.2f}")
                st.metric("Total Providers", f"{len(rates):,}")
            
            with col2:
                st.markdown("### 📈 Rate Distribution Chart")
                fig, ax = plt.subplots(figsize=(10, 6))
                
                plt.hist(rates, bins=25, alpha=0.7, color='skyblue', edgecolor='navy', linewidth=1.5)
                plt.title(f'How Much Do Providers Charge for CPT {cpt_code}?\nDistribution of Rates Across {len(rates):,} Healthcare Providers', 
                         fontsize=14, fontweight='bold')
                plt.xlabel('Cost in US Dollars', fontsize=12, fontweight='bold')
                plt.ylabel('Number of Providers', fontsize=12, fontweight='bold')
                
                ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
                plt.grid(True, alpha=0.3, linestyle='--')
                plt.xlim(rates.min() * 0.95, rates.quantile(0.95) * 1.05)
                plt.tight_layout()
                
                st.pyplot(fig)
                plt.close()
    
    # Billing Class Analysis Preview
    if 'billing_class' in df.columns:
        st.markdown("## 🏥 Billing Class Analysis")
        
        billing_counts = df['billing_class'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Service Type Breakdown")
            for class_name, count in billing_counts.items():
                percentage = (count / len(df)) * 100
                st.write(f"**{class_name}:** {count} providers ({percentage:.1f}%)")
        
        with col2:
            if 'negotiated_rate' in df.columns:
                st.markdown("### Rate Comparison by Service Type")
                for class_name in billing_counts.index:
                    class_rates = df[df['billing_class'] == class_name]['negotiated_rate']
                    st.write(f"**{class_name} Average:** ${class_rates.mean():.2f}")
    
    # Contract Type Analysis Preview
    if 'negotiated_type' in df.columns:
        st.markdown("## 📋 Contract Type Analysis")
        
        neg_type_counts = df['negotiated_type'].value_counts()
        
        st.markdown("### Payment Contract Types")
        for neg_type, count in neg_type_counts.items():
            percentage = (count / len(df)) * 100
            st.write(f"**{neg_type}:** {count} providers ({percentage:.1f}%)")
    
    # Geographic Distribution Preview
    if 'city' in df.columns:
        st.markdown("## 🌍 Geographic Distribution")
        
        city_stats = df['city'].value_counts().sort_values(ascending=False)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Geographic Summary")
            st.write(f"**Total Cities:** {len(city_stats)}")
            st.write(f"**Top City:** {city_stats.index[0]} ({city_stats.iloc[0]} providers)")
            
            st.markdown("### Top 10 Cities")
            for i, (city, count) in enumerate(city_stats.head(10).items(), 1):
                percentage = (count / len(df)) * 100
                st.write(f"{i}. **{city}:** {count} providers ({percentage:.1f}%)")
        
        with col2:
            st.markdown("### Average Negotiated Rate by City")
            if 'negotiated_rate' in df.columns:
                top_15_cities = city_stats.head(15)
                city_avg_rates = []
                city_names = []
                
                for city in top_15_cities.index:
                    city_df = df[df['city'] == city]
                    if len(city_df) > 0:
                        avg_rate = city_df['negotiated_rate'].mean()
                        city_avg_rates.append(avg_rate)
                        city_names.append(city)
                
                fig, ax = plt.subplots(figsize=(12, 6))
                bars = plt.bar(range(len(city_names)), city_avg_rates, 
                              color='gold', edgecolor='darkorange', linewidth=2)
                
                plt.title(f'Average Negotiated Rate for CPT {cpt_code} by City\nTop 15 Cities by Provider Count', 
                         fontsize=12, fontweight='bold')
                plt.xlabel('Cities', fontsize=10, fontweight='bold')
                plt.ylabel('Average Negotiated Rate ($)', fontsize=10, fontweight='bold')
                plt.xticks(range(len(city_names)), city_names, rotation=45, ha='right')
                plt.grid(True, alpha=0.3, axis='y', linestyle='--')
                
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
                
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height + 50,
                            f'${height:,.0f}', ha='center', va='bottom', 
                            fontsize=8, fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
    
    st.markdown("---")
    st.success("✅ Preview Complete! If everything looks good, you can download the PDF report below.")
    
    return True

def main():
    """Streamlit interface for custom report generation"""
    st.set_page_config(page_title="User-Friendly CPT Report Generator with Preview", page_icon="📊")
    
    st.title("📊 User-Friendly CPT Analysis Report Generator")
    st.markdown("Generate a comprehensive PDF report with **easy-to-understand charts and explanations**")
    
    st.info("🎯 **NEW**: This version includes preview functionality - see your report before downloading!")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your cleaned CPT CSV file",
        type=['csv'],
        help="Upload the cleaned CSV file containing CPT data"
    )
    
    # Option to use existing file
    if st.checkbox("Use sample data file: sample_data.csv"):
        file_path = "sample_data.csv"
        
        # Add preview button
        if st.button("👀 Preview Report", type="secondary", use_container_width=True):
            with st.spinner("Loading data and generating preview..."):
                try:
                    preview_success = show_report_preview(file_path)
                    if preview_success:
                        st.session_state.preview_ready = True
                except Exception as e:
                    st.error(f"❌ Error generating preview: {str(e)}")
        
        # Show download button only after preview
        if st.session_state.get('preview_ready', False):
            if st.button("📥 Download PDF Report", type="primary", use_container_width=True):
                with st.spinner("Generating PDF report..."):
                    try:
                        report_buffer = generate_custom_cpt_report(file_path)
                        
                        if report_buffer:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"user_friendly_cpt_27130_analysis_{timestamp}.pdf"
                            
                            st.download_button(
                                label="📥 Download User-Friendly Report (PDF)",
                                data=report_buffer,
                                file_name=filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                            
                            st.success("✅ PDF report ready for download!")
                        else:
                            st.error("❌ Failed to generate report")
                            
                    except Exception as e:
                        st.error(f"❌ Error generating report: {str(e)}")
    
    elif uploaded_file is not None:
        # Handle uploaded file
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            df = pd.read_csv(temp_file_path)
            st.success(f"✅ File uploaded successfully!")
            st.info(f"📋 Records: {len(df):,} | Columns: {len(df.columns)}")
            
            # Preview data
            st.markdown("### 👀 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Add preview button for uploaded file
            if st.button("👀 Preview Report", type="secondary", use_container_width=True, key="preview_uploaded"):
                with st.spinner("Loading data and generating preview..."):
                    try:
                        preview_success = show_report_preview(temp_file_path)
                        if preview_success:
                            st.session_state.preview_ready_uploaded = True
                    except Exception as e:
                        st.error(f"❌ Error generating preview: {str(e)}")
            
            # Show download button only after preview
            if st.session_state.get('preview_ready_uploaded', False):
                if st.button("📥 Download PDF Report", type="primary", use_container_width=True, key="download_uploaded"):
                    with st.spinner("Generating PDF report..."):
                        try:
                            report_buffer = generate_custom_cpt_report(temp_file_path)
                            
                            if report_buffer:
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                cpt_code = df['billing_code'].iloc[0] if 'billing_code' in df.columns else "Unknown"
                                filename = f"user_friendly_cpt_{cpt_code}_report_{timestamp}.pdf"
                                
                                st.download_button(
                                    label="📥 Download User-Friendly Report (PDF)",
                                    data=report_buffer,
                                    file_name=filename,
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                                
                                st.success("✅ PDF report ready for download!")
                            else:
                                st.error("❌ Failed to generate report")
                                
                        except Exception as e:
                            st.error(f"❌ Error generating report: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

if __name__ == "__main__":
    main()
