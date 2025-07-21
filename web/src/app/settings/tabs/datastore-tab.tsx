import { Plus } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { Button } from "~/components/ui/button";
import { Input } from "~/components/ui/input";
import type { Tab } from "./types";
import { useDatastoreStore, loadDatastores } from "~/core/store/datastore-store";
import { createDatastore } from "~/core/api";
import { useSettingsStore } from "~/core/store";

export const DatastoreTab: Tab = () => {
  const t = useTranslations("settings.datastore");
  const datastores = useDatastoreStore((s) => s.datastores);
  const selected = useSettingsStore((s) => s.general.selectedDatasets);
  const [name, setName] = useState("");
  const [files, setFiles] = useState<FileList | null>(null);

  useEffect(() => {
    loadDatastores();
  }, []);

  async function handleCreate() {
    if (!name || !files) return;
    await createDatastore(name, Array.from(files));
    setName("");
    loadDatastores();
  }

  const toggle = (id: string) => {
    const current = new Set(selected);
    if (current.has(id)) current.delete(id);
    else current.add(id);
    useSettingsStore.setState((s) => ({
      general: { ...s.general, selectedDatasets: Array.from(current) },
      mcp: s.mcp,
    }));
  };

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-lg font-medium">{t("title")}</h1>
      <div className="flex items-center gap-2">
        <Input value={name} onChange={(e) => setName(e.target.value)} placeholder={t("name")}/>
        <Input type="file" multiple onChange={(e) => setFiles(e.target.files)} />
        <Button onClick={handleCreate} size="icon">
          <Plus />
        </Button>
      </div>
      <ul className="flex flex-col gap-2">
        {datastores.map((d) => (
          <li key={d.id} className="flex items-center gap-2">
            <input type="checkbox" checked={selected.includes(d.id)} onChange={() => toggle(d.id)} />
            <span>{d.name}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};
DatastoreTab.icon = Plus;
DatastoreTab.displayName = "Datastore";
