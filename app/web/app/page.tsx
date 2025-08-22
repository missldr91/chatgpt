"use client";
import { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

const api = axios.create({ baseURL: process.env.NEXT_PUBLIC_SVC_URL || 'http://localhost:8000' });

export default function Home() {
  const [templateId, setTemplateId] = useState<string|undefined>();
  const [sourceId, setSourceId] = useState<string|undefined>();
  const [plan, setPlan] = useState<any>();
  const [jobId, setJobId] = useState<string|undefined>();

  const onTemplateDrop = (files:File[])=>{
    const form = new FormData();
    form.append('template', files[0]);
    api.post('/templates/ingest', form).then(r=>setTemplateId(r.data.template_id));
  };
  const onSourceDrop = (files:File[])=>{
    if(!templateId) return;
    const form = new FormData();
    form.append('template_id', templateId);
    form.append('source', files[0]);
    api.post('/sources/ingest', form).then(r=>setSourceId(r.data.source_id));
  };

  const planCall = ()=>{
    if(!templateId||!sourceId) return;
    api.post('/transform/plan', {template_id:templateId, source_id:sourceId}).then(r=>setPlan(r.data));
  };

  const execute = ()=>{
    if(!plan) return;
    api.post('/transform/execute', {plan_id:plan.plan_id}).then(r=>setJobId(r.data.job_id));
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Deck Transformer</h1>
      <section className="my-4">
        <h2>1. Upload Template</h2>
        <Dropzone onDrop={onTemplateDrop} disabled={!!templateId} />
        {templateId && <p>Template ID: {templateId}</p>}
      </section>
      <section className="my-4">
        <h2>2. Upload Source</h2>
        <Dropzone onDrop={onSourceDrop} disabled={!templateId || !!sourceId} />
        {sourceId && <p>Source ID: {sourceId}</p>}
      </section>
      <section className="my-4">
        <button className="bg-blue-500 text-white px-4 py-2" onClick={planCall} disabled={!sourceId}>Plan</button>
        {plan && <pre className="bg-gray-100 p-2 mt-2">{JSON.stringify(plan.slides, null, 2)}</pre>}
      </section>
      <section className="my-4">
        <button className="bg-green-500 text-white px-4 py-2" onClick={execute} disabled={!plan}>Export</button>
        {jobId && <p>Job ID: {jobId}</p>}
      </section>
    </div>
  );
}

function Dropzone({onDrop, disabled}:{onDrop:(files:File[])=>void, disabled?:boolean}){
  const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop: accepted=>onDrop(accepted)});
  return (
    <div {...getRootProps()} className={`border-dashed border p-4 text-center ${disabled?'opacity-50':''}`}>
      <input {...getInputProps()} disabled={disabled}/>
      {isDragActive ? <p>Drop files here...</p> : <p>Drag & drop file or click</p>}
    </div>
  );
}
