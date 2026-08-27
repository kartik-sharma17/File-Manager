"use client";

import { useRef, useState } from "react";
import { toast } from "sonner";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Progress } from "@/components/ui/progress";
import { useConfirmUploadMutation, useCreateUploadRequestMutation } from "@/redux/service/documentService";
import { uploadFileToPresignedUrl } from "@/lib/upload-file";
import { formatBytes } from "@/lib/utils";
import { FileIcon, Loader2, UploadCloud, X } from "lucide-react";

type UploadDialogProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

type UploadStage = "idle" | "requesting" | "uploading" | "confirming" | "done" | "error";

export function UploadDialog({ open, onOpenChange }: UploadDialogProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const [file, setFile] = useState<File | null>(null);
  const [isPublic, setIsPublic] = useState(false);
  const [stage, setStage] = useState<UploadStage>("idle");
  const [progress, setProgress] = useState(0);
  const [errorMessage, setErrorMessage] = useState("");

  const [createUploadRequest] = useCreateUploadRequestMutation();
  const [confirmUpload] = useConfirmUploadMutation();

  const isBusy = stage === "requesting" || stage === "uploading" || stage === "confirming";

  const resetState = () => {
    setFile(null);
    setIsPublic(false);
    setStage("idle");
    setProgress(0);
    setErrorMessage("");
  };

  const handleOpenChange = (next: boolean) => {
    if (isBusy) return; // don't let it close mid-upload
    if (!next) resetState();
    onOpenChange(next);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) setFile(selected);
  };

  const handleUpload = async () => {
    if (!file) return;

    try {
      // Step 1: request a presigned upload URL
      setStage("requesting");
      const requestRes = await createUploadRequest({
        file_name: file.name,
        mime_type: file.type || "application/octet-stream",
        size: file.size,
        is_public: isPublic,
      }).unwrap();

      const { document_id, upload_url } = requestRes.data;

      // Step 2: upload the file directly to storage
      setStage("uploading");
      await uploadFileToPresignedUrl(upload_url, file, setProgress);

      // Step 3: confirm the upload with the backend
      setStage("confirming");
      await confirmUpload(document_id).unwrap();

      setStage("done");
      toast.success(`${file.name} uploaded`);
      resetState();
      onOpenChange(false);
    } catch (err) {
      setStage("error");
      const message =
        (err as { data?: {detail?: { message?: string } }  })?.data?.detail?.message ??
        "Invalid email or password";
      toast.error(message);
    }
  };

  const stageLabel: Record<UploadStage, string> = {
    idle: "",
    requesting: "Preparing upload…",
    uploading: `Uploading… ${progress}%`,
    confirming: "Finalizing…",
    done: "Done",
    error: "Something went wrong",
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Upload document</DialogTitle>
          <DialogDescription>
            Choose a file and decide who can see it.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-5">
          {!file ? (
            <button
              type="button"
              onClick={() => inputRef.current?.click()}
              className="flex w-full flex-col items-center justify-center gap-2 rounded-md border border-dashed border-border py-10 text-muted-foreground transition-colors hover:border-foreground hover:text-foreground"
            >
              <UploadCloud className="h-6 w-6" strokeWidth={1.5} />
              <span className="text-sm font-medium">Click to choose a file</span>
            </button>
          ) : (
            <div className="flex items-center gap-3 rounded-md border border-border p-3">
              <FileIcon className="h-5 w-5 shrink-0 text-muted-foreground" strokeWidth={1.5} />
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium">{file.name}</p>
                <p className="text-xs text-muted-foreground">{formatBytes(file.size)}</p>
              </div>
              {!isBusy && stage !== "done" && (
                <button
                  type="button"
                  onClick={() => setFile(null)}
                  className="text-muted-foreground hover:text-foreground"
                >
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>
          )}

          <input
            ref={inputRef}
            type="file"
            className="hidden"
            onChange={handleFileSelect}
          />

          <div className="flex items-center justify-between rounded-md border border-border px-3 py-3">
            <div>
              <Label htmlFor="is-public" className="text-sm font-medium">
                Make public
              </Label>
              <p className="text-xs text-muted-foreground">
                Anyone with a share link can view it.
              </p>
            </div>
            <Switch
              id="is-public"
              checked={isPublic}
              onCheckedChange={setIsPublic}
              disabled={isBusy}
            />
          </div>

          {(stage === "requesting" || stage === "uploading" || stage === "confirming") && (
            <div className="space-y-2">
              <Progress value={stage === "uploading" ? progress : 100} />
              <p className="flex items-center gap-2 text-xs text-muted-foreground">
                <Loader2 className="h-3 w-3 animate-spin" />
                {stageLabel[stage]}
              </p>
            </div>
          )}

          {stage === "error" && (
            <p className="text-sm text-destructive">{errorMessage}</p>
          )}
        </div>

        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => handleOpenChange(false)}
            disabled={isBusy}
          >
            Cancel
          </Button>
          <Button onClick={handleUpload} disabled={!file || isBusy}>
            {isBusy && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Upload
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
