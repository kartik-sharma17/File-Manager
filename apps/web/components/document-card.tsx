import { Badge } from "@/components/ui/badge";
import { DocumentActionsMenu } from "@/components/document-actions-menu";
import { DocumentListItem } from "@/redux/service/documentService";
import { formatBytes, formatDate } from "@/lib/utils";
import { FileText, FileImage, FileSpreadsheet, File as FileIcon } from "lucide-react";

function getFileIcon(mimeType: string) {
  if (mimeType.startsWith("image/")) return FileImage;
  if (mimeType.includes("sheet") || mimeType.includes("csv")) return FileSpreadsheet;
  if (mimeType.includes("pdf") || mimeType.includes("text")) return FileText;
  return FileIcon;
}

export function DocumentCard({
  document,
  currentFolderId = null,
}: {
  document: DocumentListItem;
  currentFolderId?: string | null;
}) {
  const Icon = getFileIcon(document.mime_type);
  const isFailed = document.status === "failed";
  const isUploading = document.status === "uploading";
  const canManage = document.status === "completed";

  return (
    <div className="flex flex-col rounded-lg border border-border bg-card p-4 transition-shadow hover:shadow-sm">
      <div className="mb-3 flex items-start justify-between">
        <div className="flex h-10 w-10 items-center justify-center rounded-md bg-secondary">
          <Icon className="h-5 w-5 text-muted-foreground" strokeWidth={1.5} />
        </div>
        {canManage && (
          <DocumentActionsMenu
            documentId={document.document_id}
            fileName={document.file_name}
            isPublic={document.is_public}
            currentFolderId={currentFolderId}
          />
        )}
      </div>

      <p className="mb-1 truncate text-sm font-medium" title={document.file_name}>
        {document.file_name}
      </p>
      <p className="mb-3 text-xs text-muted-foreground">
        {formatBytes(document.size)} · {formatDate(document.updated_at ?? document.created_at)}
      </p>

      <div className="mt-auto flex flex-wrap gap-2">
        {isFailed && (
          <Badge className="bg-destructive text-destructive-foreground hover:bg-destructive">
            Failed
          </Badge>
        )}
        {isUploading && <Badge variant="secondary">Uploading</Badge>}
        {document.is_public && !isFailed && (
          <Badge className="bg-destructive text-destructive-foreground hover:bg-destructive">
            Public
          </Badge>
        )}
      </div>
    </div>
  );
}