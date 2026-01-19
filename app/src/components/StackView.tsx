import type { Layer, ArchitecturalPrinciple } from '../types/library';
import type { PrincipleState } from '../types/userState';

interface StackViewProps {
  layers: Layer[];
  architecturalPrinciples: ArchitecturalPrinciple[];
  getPrincipleState: (principleId: string) => PrincipleState;
  onPrincipleClick: (principleId: string) => void;
}

const layerColors: Record<string, { bg: string; border: string; text: string }> = {
  identity: { bg: 'bg-indigo-50', border: 'border-indigo-400', text: 'text-indigo-700' },
  orientation: { bg: 'bg-violet-50', border: 'border-violet-400', text: 'text-violet-700' },
  flow: { bg: 'bg-purple-50', border: 'border-purple-400', text: 'text-purple-700' },
  structure: { bg: 'bg-fuchsia-50', border: 'border-fuchsia-400', text: 'text-fuchsia-700' },
  work: { bg: 'bg-pink-50', border: 'border-pink-400', text: 'text-pink-700' },
};

const statusStyles: Record<string, string> = {
  'unexplored': 'bg-gray-100 text-gray-500 border-gray-300',
  'in-progress': 'bg-amber-100 text-amber-700 border-amber-400',
  'stance-taken': 'bg-emerald-100 text-emerald-700 border-emerald-400',
};

export function StackView({
  layers,
  architecturalPrinciples,
  getPrincipleState,
  onPrincipleClick,
}: StackViewProps) {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">AI Transformation Architecture</h1>
      <p className="text-gray-600 mb-8">
        Click on a principle to explore case studies and develop your organization's stance.
      </p>

      <div className="space-y-4">
        {layers.map((layer) => {
          const colors = layerColors[layer.id] || layerColors.identity;
          const principles = architecturalPrinciples.filter((p) => p.layerId === layer.id);

          return (
            <div
              key={layer.id}
              className={`${colors.bg} ${colors.border} border-l-4 rounded-lg p-4`}
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h2 className={`text-lg font-semibold ${colors.text}`}>{layer.name}</h2>
                  <p className="text-sm text-gray-600">{layer.description}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {principles.map((principle) => {
                  const state = getPrincipleState(principle.id);
                  const isAvailable = principle.status === 'available';

                  return (
                    <button
                      key={principle.id}
                      onClick={() => isAvailable && onPrincipleClick(principle.id)}
                      disabled={!isAvailable}
                      className={`
                        text-left p-3 rounded-md border-2 transition-all
                        ${isAvailable
                          ? `${statusStyles[state.status]} hover:shadow-md cursor-pointer`
                          : 'bg-gray-50 text-gray-400 border-gray-200 cursor-not-allowed'
                        }
                      `}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-medium">{principle.name}</span>
                        {!isAvailable && (
                          <span className="text-xs bg-gray-200 text-gray-500 px-2 py-0.5 rounded">
                            Coming Soon
                          </span>
                        )}
                        {isAvailable && state.status === 'stance-taken' && (
                          <span className="text-xs bg-emerald-200 text-emerald-700 px-2 py-0.5 rounded">
                            Done
                          </span>
                        )}
                        {isAvailable && state.status === 'in-progress' && (
                          <span className="text-xs bg-amber-200 text-amber-700 px-2 py-0.5 rounded">
                            In Progress
                          </span>
                        )}
                      </div>
                      <p className="text-xs mt-1 opacity-75">{principle.coreQuestion}</p>
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-8 p-4 bg-gray-100 rounded-lg">
        <h3 className="font-semibold text-gray-700 mb-2">Progress Legend</h3>
        <div className="flex flex-wrap gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-gray-100 border-2 border-gray-300"></div>
            <span className="text-gray-600">Unexplored</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-amber-100 border-2 border-amber-400"></div>
            <span className="text-gray-600">In Progress</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-emerald-100 border-2 border-emerald-400"></div>
            <span className="text-gray-600">Stance Taken</span>
          </div>
        </div>
      </div>
    </div>
  );
}
