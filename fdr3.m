function [fdrArrayOrgOrder] = fdr3(pvals)
% fdr3 Calculates the False Discovery Rate (FDR) corrected p-values.
% Written by: Christopher Tyler Short
%
%   This function implements the Benjamini-Hochberg procedure to control the
%   FDR, which is the expected proportion of false positives among all
%   significant results. It takes a vector of p-values, sorts them, 
%   calculates the FDR corrected p-values, and then returns the corrected 
%   p-values in the original input order.  It handles both row and column
%   vectors, preserving the original input shape.
%
%   Args:
%       pvals: A 1xN or Nx1 vector of uncorrected p-values.
%
%   Returns:
%       fdrArrayOrgOrder: A vector of the same size and orientation (row or
%                         column) as pvals, containing the FDR corrected
%                         p-values in the same order as the input pvals.
%
%   Algorithm:
%       1. Determine the input shape (row or column).
%       2. Reshape p-values to a row vector for processing.
%       3. Sort the p-values in ascending order.
%       4. For each p-value, calculate the FDR corrected p-value using the
%          formula: 
%             FDR_corrected_p = p_value * (total_number_of_p_values / rank_of_p_value)
%       5. Ensure the corrected p-values are monotonically increasing 
%          (from largest to smallest p-value) by setting each corrected 
%          p-value to the minimum of itself and the previously calculated 
%          corrected p-value.
%       6. Restore the original order of the corrected p-values.
%       7. Reshape the output to match the original input shape.
%
%   Example:
%       pvalues_row = [0.01, 0.05, 0.001, 0.02, 0.1];
%       corrected_pvalues_row = fdr2(pvalues_row);
%
%       pvalues_col = [0.01; 0.05; 0.001; 0.02; 0.1];
%       corrected_pvalues_col = fdr2(pvalues_col);
%
%   Notes:
%       - The Benjamini-Hochberg procedure is less conservative than 
%         Bonferroni correction and is suitable when testing multiple 
%         hypotheses.
%       - The function handles ties in p-values by assigning them the same 
%         rank.
%       - The monotonicity enforcement ensures that a larger p-value never 
%         has a smaller corrected p-value.

    % Determine input shape
    isRow = isrow(pvals);
    originalSize = size(pvals); %store for reshaping later

    % Find nans
    nanIndices = isnan(pvals);
    validPvals = pvals(~nanIndices);

    % Calculate FDR on valid p-values
    correctedValidPvals = fdr_no_nans(validPvals); % See helper function below

    % Reconstruct the output array
    fdrArrayOrgOrder = NaN(originalSize); % Initialize with NaNs
    % Fill in the non-nan values
    fdrArrayOrgOrder(~nanIndices) = correctedValidPvals;


    function [fdrArrayOrgOrder] = fdr_no_nans(pvals)

        pvalsLen = length(pvals);

        % Reshape to row vector for processing
        pvals = reshape(pvals, 1, []);
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
end