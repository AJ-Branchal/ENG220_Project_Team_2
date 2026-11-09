%% CATEGORY 2: FIREARM DEATHS AND VIOLENCE

% Age-adjusted firearm death rates per 100,000 people
% Figures are taken from the project proposal.

locations = categorical(["New Mexico", "United States"]);
locations = reordercats(locations, ...
    ["New Mexico", "United States"]);

firearmDeathRates = [26.6, 12.8];

figure;
bar(locations, firearmDeathRates);

title('Firearm Death Rates: New Mexico vs. United States');
xlabel('Location');
ylabel('Age-Adjusted Deaths per 100,000 People');

grid on;

% Add value labels above each bar.
hold on;

for i = 1:length(firearmDeathRates)
    text(i, firearmDeathRates(i), ...
        sprintf('%.1f', firearmDeathRates(i)), ...
        'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'bottom');
end

hold off;

% Year: 2024
% Sources listed in proposal: USAFacts, KFF, and Pew Research Center.
% Verify the figures against the original sources before publication.