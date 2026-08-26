"use client";

import { useMemo, useState } from "react";
import { useGetAllDocumentsQuery } from "@/redux/service/documentService";
import { useUploadDialog } from "@/contexts/upload-dialog-context";
import { DocumentCard } from "@/components/document-card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { formatBytes } from "@/lib/utils";
import { FileStack, HardDrive, Globe, Search, UploadCloud } from "lucide-react";

export default function DashboardPage() {
  const { data, isLoading, isError } = useGetAllDocumentsQuery();
  const { openDialog } = useUploadDialog();
  const [search, setSearch] = useState("");

  const documents = useMemo(() => data?.data ?? [], [data]);

  const stats = useMemo(() => {
    const totalDocuments = documents.length;
    const totalBytes = documents.reduce((sum, doc) => sum + (doc.size || 0), 0);
    const publicDocuments = documents.filter((doc) => doc.is_public).length;
    return { totalDocuments, totalBytes, publicDocuments };
  }, [documents]);

  const filteredDocuments = useMemo(() => {
    if (!search.trim()) return documents;
    return documents.filter((doc) =>
      doc.file_name.toLowerCase().includes(search.trim().toLowerCase())
    );
  }, [documents, search]);

  return (
    <div className="mx-auto max-w-6xl">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="font-display text-3xl">DASHBOARD</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Everything you&apos;ve uploaded, in one place.
          </p>
        </div>
        <Button onClick={openDialog} className="gap-2">
          <UploadCloud className="h-4 w-4" />
          Upload document
        </Button>
      </div>

      {/* Stat cards */}
      <div className="mb-10 grid gap-4 sm:grid-cols-3">
        <StatCard
          icon={FileStack}
          label="Documents uploaded"
          value={isLoading ? null : String(stats.totalDocuments)}
        />
        <StatCard
          icon={HardDrive}
          label="Storage used"
          value={isLoading ? null : formatBytes(stats.totalBytes)}
        />
        <StatCard
          icon={Globe}
          label="Public documents"
          value={isLoading ? null : String(stats.publicDocuments)}
        />
      </div>

      {/* Search */}
      <div className="mb-6 flex items-center justify-between gap-4">
        <h2 className="text-lg font-semibold">Your documents</h2>
        <div className="relative w-full max-w-xs">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search documents…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      {/* Document grid */}
      {isLoading ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-32 rounded-lg" />
          ))}
        </div>
      ) : isError ? (
        <div className="rounded-lg border border-border py-16 text-center text-sm text-muted-foreground">
          Couldn&apos;t load your documents. Try refreshing the page.
        </div>
      ) : filteredDocuments.length === 0 ? (
        <div className="rounded-lg border border-dashed border-border py-16 text-center">
          <p className="text-sm font-medium">
            {search ? "No documents match your search." : "No documents yet."}
          </p>
          {!search && (
            <Button variant="outline" className="mt-4" onClick={openDialog}>
              Upload your first document
            </Button>
          )}
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filteredDocuments.map((document) => (
            <DocumentCard key={document.document_id} document={document} />
          ))}
        </div>
      )}
    </div>
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
}: {
  icon: React.ElementType;
  label: string;
  value: string | null;
}) {
  return (
    <div className="rounded-lg border border-border p-5">
      <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-md bg-secondary">
        <Icon className="h-5 w-5" strokeWidth={1.5} />
      </div>
      {value === null ? (
        <Skeleton className="h-7 w-16" />
      ) : (
        <p className="font-display text-2xl">{value}</p>
      )}
      <p className="mt-1 text-sm text-muted-foreground">{label}</p>
    </div>
  );
}
