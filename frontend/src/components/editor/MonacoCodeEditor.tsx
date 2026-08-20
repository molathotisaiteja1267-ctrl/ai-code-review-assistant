import React, { useRef, useEffect } from 'react';
import Editor, { Monaco, OnMount } from '@monaco-editor/react';
import { ReviewIssue } from '../../types';

interface MonacoCodeEditorProps {
  code: string;
  language?: string;
  issues?: ReviewIssue[];
  selectedIssue?: ReviewIssue | null;
  onSelectIssue?: (issue: ReviewIssue) => void;
  readOnly?: boolean;
  onChange?: (val: string) => void;
}

export const MonacoCodeEditor: React.FC<MonacoCodeEditorProps> = ({
  code,
  language = 'python',
  issues = [],
  selectedIssue = null,
  onSelectIssue,
  readOnly = false,
  onChange
}) => {
  const editorRef = useRef<any>(null);
  const monacoRef = useRef<Monaco | null>(null);
  const decorationsRef = useRef<string[]>([]);

  const handleEditorDidMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    updateDecorations();
  };

  const updateDecorations = () => {
    if (!editorRef.current || !monacoRef.current) return;
    const monaco = monacoRef.current;
    const editor = editorRef.current;

    const newDecorations = issues.map((issue) => {
      let className = 'monaco-low-line';
      if (issue.severity === 'critical') className = 'monaco-critical-line';
      else if (issue.severity === 'high') className = 'monaco-high-line';
      else if (issue.severity === 'medium') className = 'monaco-medium-line';

      return {
        range: new monaco.Range(issue.line_start, 1, issue.line_end, 1),
        options: {
          isWholeLine: true,
          className: className,
          hoverMessage: {
            value: `**[${issue.severity.toUpperCase()}] ${issue.title}**\n\n${issue.explanation}\n\n*Impact*: ${issue.impact || 'N/A'}`
          }
        }
      };
    });

    decorationsRef.current = editor.deltaDecorations(decorationsRef.current, newDecorations);
  };

  useEffect(() => {
    updateDecorations();
  }, [issues, code]);

  useEffect(() => {
    if (selectedIssue && editorRef.current) {
      editorRef.current.revealLineInCenter(selectedIssue.line_start);
      editorRef.current.setPosition({ lineNumber: selectedIssue.line_start, column: 1 });
    }
  }, [selectedIssue]);

  return (
    <div className="h-full w-full rounded-xl overflow-hidden border border-surface-border bg-white shadow-subtle">
      <Editor
        height="100%"
        language={language}
        value={code}
        theme="vs"
        options={{
          readOnly: readOnly,
          minimap: { enabled: false },
          fontSize: 13,
          lineNumbers: 'on',
          glyphMargin: false,
          folding: true,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          renderValidationDecorations: 'on',
          fontFamily: "'JetBrains Mono', 'Fira Code', Consolas, monospace",
          lineHeight: 20,
        }}
        onMount={handleEditorDidMount}
        onChange={(val) => onChange && onChange(val || '')}
      />
    </div>
  );
};
