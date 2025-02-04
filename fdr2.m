function [fdrArrayOrgOrder] = fdr2(pvals)
% fdr2 Calculates the False Discovery Rate (FDR) corrected p-values.
%
%   This function implements the Benjamini-Hochberg procedure to control the
%   FDR, which is the expected proportion of false positives among all
%   significant results. It takes a vector of p-values, sorts them, 
%   calculates the FDR corrected p-values, and then returns the corrected 
%   p-values in the original input order.
%
%   Args:
%       pvals: A 1xN or Nx1 vector of uncorrected p-values.
%
%   Returns:
%       fdrArrayOrgOrder: A vector of the same size as pvals containing the
%                         FDR corrected p-values in the same order as the
%                         input pvals.
%
%   Algorithm:
%       1. Sort the p-values in ascending order.
%       2. For each p-value, calculate the FDR corrected p-value using the
%          formula: 
%             FDR_corrected_p = p_value * (total_number_of_p_values / rank_of_p_value)
%       3. Ensure the corrected p-values are monotonically increasing 
%          (from largest to smallest p-value) by setting each corrected 
%          p-value to the minimum of itself and the previously calculated 
%          corrected p-value.
%       4. Restore the original order of the corrected p-values.
%
%   Example:
%       pvalues = [0.01, 0.05, 0.001, 0.02, 0.1];
%       corrected_pvalues = fdr2(pvalues);
%
%   Notes:
%       - The Benjamini-Hochberg procedure is less conservative than 
%         Bonferroni correction and is suitable when testing multiple 
%         hypotheses.
%       - The function handles ties in p-values by assigning them the same 
%         rank.
%       - The monotonicity enforcement ensures that a larger p-value never 
%         has a smaller corrected p-value.
%       

    pvalsLen = length(pvals);
    % Sort p-values and store original indices
    [pvalsSort, pvalsI] = sort(pvals);
    
    % Initialize the array to store FDR corrected p-values
    fdrArray = zeros(1, pvalsLen);
    
    % Initialize previous FDR for monotonicity enforcement
    prevFDR = 1; 
    
    % Iterate through p-values from largest to smallest
    for i = pvalsLen:-1:1
        pVal = pvalsSort(i);
        pValRank = i; % The rank of the current p-value (1-based index)
        
        % Calculate the FDR corrected p-value
        fdr_pval = pVal * (pvalsLen / pValRank);
        
        % Enforce monotonicity: corrected p-value should not be greater than the previous one
        fdr_pval = min(fdr_pval, prevFDR); 
        
        % Store the corrected p-value
        fdrArray(i) = fdr_pval;
        
        % Update the previous FDR value
        prevFDR = fdr_pval;
    end
    
    % Restore the original order of the corrected p-values
    [~, inv_pvalsI] = sort(pvalsI);
    fdrArrayOrgOrder = fdrArray(inv_pvalsI);
end