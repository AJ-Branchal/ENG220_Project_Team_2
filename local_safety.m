%% CATEGORY 3: LOCAL SAFETY AND COMMUNITY RESOURCES

% Number of sources listed for each topic in the proposal.
% These counts measure research coverage, NOT safety or crime levels.

topics = [
    "Wildlife Crossings and Road Safety"
    "Police Department"
    "Sexual Assault Reporting"
    "Public Records Requests"
    "Government Audit"
    "Visitor Information"
];

sourceCounts = [3, 1, 1, 1, 1, 1];

figure;
barh(sourceCounts);

yticks(1:length(topics));
yticklabels(topics);

title('Local Safety Research: Sources by Topic');
xlabel('Number of Sources Listed');
ylabel('Local Safety Topic');

grid on;

% The three wildlife-crossing sources are:
% NMDOT, Wildlands Network, and KRQE.
%
% The remaining counts represent individual sources
% listed in the project proposal.
%
% This graph measures the distribution of research sources.
% It does not measure crime, danger, or project effectiveness.