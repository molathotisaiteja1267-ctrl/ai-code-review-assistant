import React from 'react';
import { DiffEditor } from '@monaco-editor/react';

interface MonacoDiffViewerProps {
  original: string;
  modified: string;
  language?: string;
}

export const MonacoDiffViewer: React.FC<MonacoDiffViewerProps> = ({
  original,
  modified,
  language = 'python'
}) => {
  return (
    <div className="h-96 w-full rounded-xl overflow-hidden border border-surface-border bg-white shadow-subtle">
      <DiffEditor
        height="100%"
        original={original}
        modified={modified}
        language={language}
        theme="vs"
        options={{
          readOnly: true,
          renderSideBySide: true,
          fontSize: 12,
          fontFamily: "'JetBrains Mono', 'Fira Code', Consolas, monospace",
          automaticLayout: true,
          lineHeight: 19,
        }}
      />
    </div>
  );
};
