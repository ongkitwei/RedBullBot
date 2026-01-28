# Prompt for generating analysis of stock
def stock_analysis_prompt(stock_name):
    prompt = f"""
                Role: Act as a Senior Equity Research Analyst specializing in Fundamental Analysis and Moat Assessment.
                Format: USE PLAIN TEXT ONLY. DO NOT USE MARKDOWN (no **, *, or _).
                Sequence: Follow this sequence of how the response should be.
                Task: Analyze the stock: ${stock_name}.

                Provide a rating out of 5 for each category based on the last 3-5 years of financial data, and have the rating placed at the top. Do not need to have description just ratings will do. For each metric, provide a rating out of 5 using star emojis (e.g., ⭐⭐⭐⭐):
                - Predictability: (Based on revenue/earnings consistency)
                - Profitability: (Based on ROIC and Net Margins)
                - Growth: (Based on 3-year Revenue/EPS CAGR)
                - Moat: (Based on competitive advantage durability)
                - Financial Strength: (Based on Debt-to-Equity and Current Ratio)
                - Valuation: (Current P/E or EV/FCF vs. 5-year historical average)

                For each factors below, provide a concise 2-sentence description of how it applies to this company and a rating out of 10, and placed the rating at the top.
                average moat score (average score of the 5 factors, Display it as: "Average Moat Score: [X]/10" have it in caps)
                1. Brand Loyalty & Pricing Power [X]/10: (Can they raise prices without losing customers?) 
                2. High Barriers to Entry [X]/10: (How hard is it for a startup to compete?) 
                3. High Switching Cost [X]/10: (How painful is it for a customer to leave?) 
                4. Network Effect [X]/10: (Does the product get better as more people use it?) 
                5. Economies of Scale [X]/10: (Do their costs drop significantly as they grow?) 

                competitive landscape (have it in caps)
                List the 3 closest competitors (Public or Private) and briefly mention one area where this stock has an advantage over them. Ensure there is line spacing between each pointers.
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