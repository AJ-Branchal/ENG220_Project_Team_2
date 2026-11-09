% Cuba, New Mexico - Reported offenses by type, 2018-2020
% Source: Uniform Crime Reports - NM Department of Public Safety
% Values are the "Number" metric (count of offenses) from Cuba_data.csv

years = [2018 2019 2020];

offenses = {'Criminal Homicide', 'Forcible Rape', 'Robbery', 'Assault', ...
            'Burglary', 'Larceny-Theft', 'Motor Vehicle Theft'};

% Rows = offense types, columns = years (2018, 2019, 2020)
counts = [ 0  0  0;    % Criminal Homicide
           0  0  0;    % Forcible Rape
           0  1  1;    % Robbery
          20 16 17;    % Assault
           7  1  5;    % Burglary
           3  0  4;    % Larceny-Theft
           0  1  1];   % Motor Vehicle Theft

% ---- Grouped bar chart: offense types, one bar per year ----
figure('Name', 'Cuba NM Crime', 'Color', 'w', 'Position', [100 100 950 550]);
b = bar(counts, 'grouped');
b(1).FaceColor = [0.20 0.45 0.75];
b(2).FaceColor = [0.95 0.60 0.20];
b(3).FaceColor = [0.35 0.70 0.40];

set(gca, 'XTickLabel', offenses, 'FontSize', 11);
xtickangle(30);
xlabel('Offense Type', 'FontSize', 12);
ylabel('Number of Offenses', 'FontSize', 12);
title('Reported Crimes by Type in Cuba, New Mexico (2018-2020)', 'FontSize', 14);
legend(string(years), 'Location', 'northeast');
grid on;
box off;

% Label each bar with its value (skip zeros to keep the chart clean)
for k = 1:numel(b)
    xt = b(k).XEndPoints;
    yt = b(k).YData;
    for i = 1:numel(yt)
        if yt(i) > 0
            text(xt(i), yt(i) + 0.3, num2str(yt(i)), ...
                'HorizontalAlignment', 'center', 'FontSize', 9);
        end
    end
end

% To save the figure, uncomment:
% exportgraphics(gcf, 'cuba_nm_crime.png', 'Resolution', 300);