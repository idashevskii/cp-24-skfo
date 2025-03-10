import { Check, Copy } from "lucide-react";
import { useMemo } from "react";
import { Button } from "../../button";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "../../hover-card";
import { useCopyToClipboard } from "../hooks/use-copy-to-clipboard";
import { SourceData } from "../index";
import PdfDialog from "../widgets/PdfDialog";

const SCORE_THRESHOLD = 0.3;

function SourceNumberButton({ index }: { index: number }) {
  return (
    <div className="text-xs w-5 h-5 rounded-full bg-gray-100 mb-2 flex items-center justify-center hover:text-white hover:bg-primary hover:cursor-pointer">
      {index + 1}
    </div>
  );
}

type NodeInfo = {
  id: string;
  url?: string;
  document_url?: string;
  document_title?: string;
};

export function ChatSources({ data }: { data: SourceData }) {
  const sources: NodeInfo[] = useMemo(() => {
    // aggregate nodes by url or file_path (get the highest one by score)
    const nodesByPath: { [path: string]: NodeInfo } = {};

    data.nodes
      .filter((node) => (node.score ?? 1) > SCORE_THRESHOLD)
      .sort((a, b) => (b.score ?? 1) - (a.score ?? 1))
      .forEach((node) => {
        const nodeInfo = {
          id: node.id,
          url: node.url,
          document_url: node.metadata?.document_url as string|undefined,
          document_title: node.metadata?.document_title as string|undefined,
        };
        const key = nodeInfo.url ?? nodeInfo.id; // use id as key for UNKNOWN type
        if (!nodesByPath[key]) {
          nodesByPath[key] = nodeInfo;
        }
      });

    return Object.values(nodesByPath);
  }, [data.nodes]);

  if (sources.length === 0) return null;

  const links=sources.map((nodeInfo: NodeInfo, index: number) => {
    if (nodeInfo.document_url){
      return <div className="mb-1 ml-0 text-sm" key={index}>
        <a className="underline" target="_blank" href={nodeInfo.document_url}>{nodeInfo.document_title||nodeInfo.document_url}</a>
      </div>
    }
    return null;
  }).filter(e=>e)

  return (
    <div>
      <div className="space-x-2 text-sm">
        <span className="font-semibold">Источники:</span>
        <div className="inline-flex gap-1 items-center">
          {sources.map((nodeInfo: NodeInfo, index: number) => {
            if (nodeInfo.url?.endsWith(".pdf")) {
              return (
                <PdfDialog
                  key={nodeInfo.id}
                  documentId={nodeInfo.id}
                  url={nodeInfo.url!}
                  trigger={<SourceNumberButton index={index} />}
                />
              );
            }
            return (
              <div key={nodeInfo.id}>
                <HoverCard>
                  <HoverCardTrigger>
                    <SourceNumberButton index={index} />
                  </HoverCardTrigger>
                  <HoverCardContent className="w-[320px]">
                    <NodeInfo nodeInfo={nodeInfo} />
                  </HoverCardContent>
                </HoverCard>
              </div>
            );
          })}
        </div>
      </div>
      {links.length ? links : undefined}
    </div>
  );
}

function NodeInfo({ nodeInfo }: { nodeInfo: NodeInfo }) {
  const { isCopied, copyToClipboard } = useCopyToClipboard({ timeout: 1000 });

  if (nodeInfo.url) {
    // this is a node generated by the web loader or file loader,
    // add a link to view its URL and a button to copy the URL to the clipboard
    return (
      <div className="flex items-center my-2">
        <a className="hover:text-blue-900" href={nodeInfo.url} target="_blank">
          <span>{nodeInfo.url}</span>
        </a>
        <Button
          onClick={() => copyToClipboard(nodeInfo.url!)}
          size="icon"
          variant="ghost"
          className="h-12 w-12 shrink-0"
        >
          {isCopied ? (
            <Check className="h-4 w-4" />
          ) : (
            <Copy className="h-4 w-4" />
          )}
        </Button>
      </div>
    );
  }

  // node generated by unknown loader, implement renderer by analyzing logged out metadata
  return (
    <p>
      Sorry, unknown node type. Please add a new renderer in the NodeInfo
      component.
    </p>
  );
}
