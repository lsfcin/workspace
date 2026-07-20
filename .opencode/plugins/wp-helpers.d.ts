export function buildPayloads(args: any, toolName: any): {
    file_path: any;
    content: string;
    old_string: string;
    new_string: string;
}[];
export function run(script: any, payload: any, canonical: any, { stdin }?: {}): any;
export function warn(client: any, msg: any): Promise<void>;
export const WORKSPACE: "/mnt/workspace";
export const HOOKS: "/mnt/workspace/.hooks";
export namespace TOOL_MAP {
    namespace read {
        let canonical: string;
        let group: string;
    }
    namespace edit {
        let canonical_1: string;
        export { canonical_1 as canonical };
        let group_1: string;
        export { group_1 as group };
    }
    namespace write {
        let canonical_2: string;
        export { canonical_2 as canonical };
        let group_2: string;
        export { group_2 as group };
    }
    namespace apply_patch {
        let canonical_3: string;
        export { canonical_3 as canonical };
        let group_3: string;
        export { group_3 as group };
    }
}
