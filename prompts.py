# Prompt for generating analysis of stock
def stock_analysis_prompt(stock_name):
    prompt = f"""
               Role: You are an expert equity research analyst and institutional investor specializing in rigorous fundamental analysis. Your task is to perform a comprehensive fundamental analysis on a stock based on the user-provided ticker. Use the latest available data, annual reports, and historical financial statements to evaluate the company against the following 12-part checklist. Ensure your analysis is objective, deeply data-driven, and avoids generic summaries.
                Format: USE PLAIN TEXT ONLY. DO NOT USE MARKDOWN (no **, *, or _).
                Sequence: Follow this sequence of how the response should be.
                Task: Analyze the stock: ${stock_name}.


### 1. Introduction to the Business
* 1a. Business Overview: What is the core business about, and what products/services do they offer?
* 1b. Revenue Model: Exactly how do they make money (break down revenue segments or geography if significant)?
* 1c. M&A Activity: Detail any notable acquisitions they own or recent corporate actions.
* 1d. Market Share: What is their current market share within their primary industry/vertical?
* 1e. Competitive Landscape: Who are their main competitors, and what is the company's distinct value proposition or how do they stand out?

### 2. Economic Moat (Rate 1 to 10)
* Evaluate the strength and type of their economic moat (e.g., network effects, switching costs, cost advantages, intangible assets). Provide a score from 1 to 10 with a detailed qualitative justification.

### 3. Pricing Power (Rate 1 to 10)
* Analyze their ability to continue raising prices while keeping their competitive edge and market share. Provide a score from 1 to 10 with historical or qualitative evidence.

### 4. Barriers to Entry (Rate 1 to 10)
* How difficult is it for new entrants to disrupt this business or replicate its infrastructure/scale? Provide a score from 1 to 10.

### 5. High Growth/Performance Consistency (Rate 1 to 10)
* Rate the overall operational performance, execution high-standards, and structural growth reliability of this company on a scale of 1 to 10.

### 6. Return on Equity (ROE) Analysis
* State the company's current Return on Equity (ROE). Explicitly analyze whether their ROE is consistently more than 15%, and discuss what this means for their capital efficiency.

### 7. Historical Free Cash Flow (FCF) Trend & Chart
* Analysis: Analyze the 5-year and 10-year trends for Free Cash Flow (FCF). Is it consistently increasing, stable, or lumpy? Provide the exact historical data points.
* Visual Chart: Generate a visual rendering of this 5/10-year trend. Use a mermaid code block (e.g., `xychart-beta`) or a well-formatted markdown horizontal bar chart so that the trend is instantly recognizable visually.

### 8. Historical Revenue Trend & Chart
* Analysis: Analyze the 5-year and 10-year trends for Top-line Revenue. Is it consistently increasing? Provide the exact historical growth figures.
* Visual Chart: Generate a visual rendering of this 5/10-year trend. Use a mermaid code block (e.g., `xychart-beta`) or a well-formatted markdown horizontal bar chart so that the trend is instantly recognizable visually.

### 9. Historical Earnings Per Share (EPS) Trend & Chart
* Analysis: Analyze the 5-year and 10-year trends for Diluted EPS. Has share dilution or share buybacks significantly impacted this metric?
* Visual Chart: Generate a visual rendering of this 5/10-year trend. Use a mermaid code block (e.g., `xychart-beta`) or a well-formatted markdown horizontal bar chart so that the trend is instantly recognizable visually.

### 10. Key Financial Metrics Dashboard
Present the following metrics clearly in a markdown table, detailing current values and brief commentary on their health:
* Margins: Gross Margin, Operating Margin, and Net Profit Margin.
* Leverage & Solvency: Debt-to-Equity (D/E) ratio, Net Debt-to-EBITDA, and Interest Coverage Ratio.
* Liquidity: Current Ratio and Quick Ratio.

### 11. Valuation Models
* PEG Ratio: Provide the current PEG ratio and state whether it implies undervaluation relative to growth.
* Discounted Cash Flow (DCF) Valuation: Run a multi-scenario DCF model. Clearly state your assumptions (Discount Rate/WACC, Terminal Growth Rate, and FCF Growth Rates) for three cases:
    * *Worst Case Scenario:* (Conservative assumptions, compressed margins, low growth) -> Calculate Intrinsic Value.
    * *Base Case Scenario:* (Most likely consensus assumptions) -> Calculate Intrinsic Value.
    * *Upside Case Scenario:* (Optimistic/Bullish assumptions, market expansion) -> Calculate Intrinsic Value.
    * Compare the current stock price against these three intrinsic values to determine the margin of safety.

### 12. Investment Thesis Summary
Conclude your analysis with three distinct, punchy summaries:
* Bull Case: What happens if everything goes perfectly?
* Bear Case: What are the key risks, structural threats, or downside triggers?
* Final Thesis: A synthesized conclusion summarizing whether the stock is a Buy, Hold, or Sell at its current valuation based on your findings.
            """ 
    return prompt

# Prompt for generating earnings summary
def earnings_summary_prompt(stock_name):
    prompt = f"""
                Role: Senior Equity Research Analyst.
                Task: Summarize the LATEST quarterly earnings for {stock_name}.
                Constraint: PLAIN TEXT ONLY. NO MARKDOWN. Be extremely concise.

                [ {stock_name.upper()} EARNINGS DASHBOARD ] (add  📊 emoji)
                ━━━━━━━━━━━━━━━━━━━━

                1. THE NUMBERS (Beat/Miss):
                - Revenue: [Actual] vs [Est]
                - EPS: [Actual] vs [Est]
                - Guidance: [Upgraded / Maintained / Downgraded]

                2. THE "RISK" (What could go wrong?):
                - [Mention 1-3 critical headwinds or negative management comments]

                3. THE "REWARD" (The Bull Case):
                - [Mention 1-3 critical tailwinds or growth drivers]

                4. CEO & MANAGEMENT INSIGHTS:
                - Key Quote: [Provide 1 high-impact quote from the CEO/CFO about future strategy]
                - Management Tone: [Briefly describe if they sounded Confident, Cautious, or Defensive during Q&A]
            """
    return prompt