export function WorkspacePolicy({ client }: {
    client: any;
}): Promise<{
    "tool.execute.before": (input: any, output: any) => Promise<void>;
    "tool.execute.after": (input: any, output: any) => Promise<void>;
}>;
