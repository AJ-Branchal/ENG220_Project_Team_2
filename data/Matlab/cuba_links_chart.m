% Cuba, New Mexico research links - count by category and geography
% Data comes from cuba_nm_links.csv (7 unique links)

categories = {'Crime & Safety Statistics', 'Local Government & Community Resources'};
geographies = {'Village of Cuba', 'Sandoval County', 'New Mexico (statewide)'};

% Rows = categories, columns = geographies
counts = [0 1 2;    % Crime & Safety Statistics
          3 1 0];   % Local Government & Community Resources

figure('Name', 'Cuba NM Links', 'Color', 'w', 'Position', [100 100 800 500]);
b = bar(counts, 'stacked');
b(1).FaceColor = [0.20 0.45 0.75];
b(2).FaceColor = [0.95 0.60 0.20];
b(3).FaceColor = [0.60 0.60 0.60];

set(gca, 'XTickLabel', categories, 'FontSize', 11, 'YTick', 0:1:5);
ylabel('Number of Links', 'FontSize', 12);
title('Cuba, NM Research Links by Category and Geography', 'FontSize', 14);
legend(geographies, 'Location', 'northeast');
grid on;
box off;

% Label each segment with its count (skip zeros)
for k = 1:numel(b)
    for i = 1:size(counts, 1)
        if counts(i, k) > 0
            ytop = sum(counts(i, 1:k));
            text(i, ytop - counts(i, k)/2, num2str(counts(i, k)), ...
                'HorizontalAlignment', 'center', 'Color', 'w', ...
                'FontWeight', 'bold', 'FontSize', 11);
        end
    end
end

% To save the figure, uncomment:
% exportgraphics(gcf, 'cuba_links_chart.png', 'Resolution', 300);
