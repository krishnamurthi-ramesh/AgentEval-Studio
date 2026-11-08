import { EvalPack } from '../types';

export function exportToPromptfooYaml(pack: EvalPack): string {
  const lines: string[] = [
    `# Promptfoo Configuration — Exported by AgentEval Studio`,
    `description: "${pack.name} (v${pack.version})"`,
    ``,
    `prompts:`,
    `  - "You are an AI assistant. Answer user prompt using tools if necessary: {{user_input}}"`,
    ``,
    `providers:`,
    `  - "openai:gpt-4o-mini"`,
    `  - "anthropic:messages:claude-3-5-haiku-20241022"`,
    ``,
    `tests:`
  ];

  for (const c of pack.cases) {
    lines.push(`  - description: "[${c.category}] ${c.id}"`);
    lines.push(`    vars:`);
    lines.push(`      user_input: "${c.user_input.replace(/"/g, '\\"')}"`);
    lines.push(`    assert:`);

    if (c.expected_trajectory.length === 0 && c.forbidden_tools && c.forbidden_tools.length > 0) {
      for (const forbidden of c.forbidden_tools) {
        lines.push(`      - type: not-contains`);
        lines.push(`        value: "${forbidden}"`);
      }
    } else if (c.expected_trajectory.length > 0) {
      for (const exp of c.expected_trajectory) {
        lines.push(`      - type: contains`);
        lines.push(`        value: "${exp.tool_name}"`);
        for (const [, v] of Object.entries(exp.arguments || {})) {
          lines.push(`      - type: contains`);
          lines.push(`        value: "${v}"`);
        }
      }
    } else {
      lines.push(`      - type: is-json`);
    }
  }

  return lines.join('\n');
}
