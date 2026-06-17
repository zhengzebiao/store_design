import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { App, Button, Card, Collapse, Empty, Form, Input, InputNumber, Layout, List, Radio, Select, Space, Spin, Switch, Typography } from 'antd'
import { getComponents } from '../../api/components'
import { getTemplateDetail } from '../../api/templates'
import { savePage } from '../../api/pages'
import type { ComponentSchemaField } from '../../domain/component'
import { createComponentFromMeta, createEmptyPage } from '../../domain/factory'
import { useEditorStore } from '../../store/editorStore'
import './editor.less'

function getByPath(target: Record<string, unknown>, path: string) {
  return path.split('.').filter(Boolean).reduce<unknown>((current, key) => {
    if (!current || typeof current !== 'object' || Array.isArray(current)) return undefined
    return (current as Record<string, unknown>)[key]
  }, target)
}

function isEmptyValue(value: unknown) {
  return value === undefined || value === null || value === '' || (Array.isArray(value) && value.length === 0)
}

function renderField(field: ComponentSchemaField, value: unknown, onChange: (value: unknown) => void) {
  const options = field.options || []
  switch (field.type) {
    case 'textarea':
      return <Input.TextArea rows={3} value={String(value ?? '')} onChange={(event) => onChange(event.target.value)} />
    case 'number':
    case 'slider':
      return <InputNumber className="store-editor__full" min={field.min} max={field.max} value={typeof value === 'number' ? value : undefined} onChange={onChange} />
    case 'color':
      return <Input type="color" value={String(value || field.default || '#ffffff')} onChange={(event) => onChange(event.target.value)} />
    case 'switch':
      return <Switch checked={Boolean(value)} onChange={onChange} />
    case 'select':
      return <Select value={value as string | number | undefined} options={options} onChange={onChange} />
    case 'radio':
      return <Radio.Group value={value} options={options} onChange={(event) => onChange(event.target.value)} />
    case 'text':
    default:
      return <Input value={String(value ?? '')} onChange={(event) => onChange(event.target.value)} />
  }
}

export default function StoreDesignEditor() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { message } = App.useApp()
  const routeId = searchParams.get('id') || ''
  const mode = (searchParams.get('mode') || 'create') as 'create' | 'edit' | 'copy'
  const store = useEditorStore()
  const { page, selectedComponentId } = store

  const detailQuery = useQuery({
    queryKey: ['template-detail', routeId],
    queryFn: () => getTemplateDetail(routeId),
    enabled: mode !== 'create' && Boolean(routeId),
  })
  const componentsQuery = useQuery({ queryKey: ['components'], queryFn: getComponents })
  const saveMutation = useMutation({
    mutationFn: savePage,
    onSuccess: (result) => {
      message.success(result.message)
      navigate(`/edit?mode=edit&id=${result.diy_id}`, { replace: true })
    },
  })

  useEffect(() => {
    store.setMode(mode)
    store.setRouteId(routeId)
    if (mode === 'create') {
      store.setPage(createEmptyPage())
    }
  }, [mode, routeId])

  useEffect(() => {
    if (detailQuery.data) {
      const nextPage = mode === 'copy'
        ? { ...detailQuery.data, id: '', diy_id: routeId, page_name: `${detailQuery.data.page_name} 副本` }
        : detailQuery.data
      store.setPage(nextPage)
    }
  }, [detailQuery.data, mode, routeId])

  const selected = page.datas.find((item) => item.id === selectedComponentId)
  const selectedMeta = componentsQuery.data?.find((item) => item.component_key === selected?.component_key)
  const schemaGroups = selectedMeta?.schema_json?.groups || []

  const handleSave = () => {
    if (!page.page_name.trim()) {
      message.error('页面名称不能为空')
      return
    }
    const invalidComponent = page.datas.find((component) => !component.id || !component.component_key || !component.component_title || !component.template_id || !component.remote_data)
    if (invalidComponent) {
      message.error(`${invalidComponent.component_title || invalidComponent.component_key} 组件数据不完整`)
      return
    }
    if (selected && selectedMeta) {
      const requiredField = schemaGroups.flatMap((group) => group.fields).find((field) => field.required && isEmptyValue(getByPath(selected.remote_data, field.key)))
      if (requiredField) {
        message.error(`${requiredField.label} 不能为空`)
        return
      }
    }
    saveMutation.mutate({ ...page, mode, route_id: routeId })
  }

  return (
    <Layout className="store-editor">
      <Layout.Header className="store-editor__toolbar">
        <Space>
          <Button onClick={() => navigate('/home')}>返回</Button>
          <Typography.Text strong>{page.page_name || '首页装修'}</Typography.Text>
          <Typography.Text type="secondary">mode={mode} route_id={routeId || '-'}</Typography.Text>
        </Space>
        <Space>
          <Button onClick={() => message.info('预览将在下一阶段完善')}>预览</Button>
          <Button type="primary" loading={saveMutation.isPending} onClick={handleSave}>保存</Button>
        </Space>
      </Layout.Header>

      <Layout className="store-editor__body">
        <Layout.Sider width={260} theme="light" className="store-editor__panel">
          <Typography.Title level={5}>组件面板</Typography.Title>
          {componentsQuery.isLoading && <Spin />}
          <List
            dataSource={componentsQuery.data || []}
            renderItem={(item) => (
              <List.Item actions={[<Button type="link" onClick={() => store.addComponent(createComponentFromMeta(item))}>添加</Button>]}>
                <List.Item.Meta title={item.name} description={item.component_key} />
              </List.Item>
            )}
          />
        </Layout.Sider>

        <Layout.Content className="store-editor__canvas-wrap">
          <div className="store-editor__canvas">
            {detailQuery.isLoading && <Spin />}
            {!detailQuery.isLoading && page.datas.length === 0 && <Empty description="从左侧添加组件" />}
            {page.datas.map((component) => (
              <Card
                key={component.id}
                size="small"
                className={component.id === selectedComponentId ? 'store-editor__component is-selected' : 'store-editor__component'}
                onClick={() => store.selectComponent(component.id)}
              >
                <Space className="store-editor__component-title">
                  <Typography.Text strong>{component.component_title}</Typography.Text>
                  <Typography.Text type="secondary">{component.component_key}</Typography.Text>
                </Space>
              </Card>
            ))}
          </div>
        </Layout.Content>

        <Layout.Sider width={340} theme="light" className="store-editor__panel">
          <Typography.Title level={5}>配置面板</Typography.Title>
          {!selected && (
            <Form layout="vertical">
              <Form.Item label="页面名称" required>
                <Input value={page.page_name} onChange={(event) => store.updatePageName(event.target.value)} />
              </Form.Item>
            </Form>
          )}
          {selected && (
            <Form layout="vertical">
              <Form.Item label="组件标题" required>
                <Input value={selected.component_title} onChange={(event) => store.updateSelectedTitle(event.target.value)} />
              </Form.Item>
              {schemaGroups.length > 0 ? (
                <Collapse
                  className="store-editor__schema"
                  defaultActiveKey={schemaGroups.map((group) => group.key)}
                  items={schemaGroups.map((group) => ({
                    key: group.key,
                    label: group.title,
                    children: group.fields.map((field) => (
                      <Form.Item key={field.key} label={field.label} required={field.required} extra={field.tips}>
                        {renderField(field, getByPath(selected.remote_data, field.key) ?? field.default, (value) => store.updateSelectedRemoteData(field.key, value))}
                      </Form.Item>
                    )),
                  }))}
                />
              ) : (
                <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="该组件暂无配置 schema" />
              )}
              <Form.Item label="调试数据">
                <Input.TextArea value={JSON.stringify(selected.remote_data, null, 2)} rows={6} readOnly />
              </Form.Item>
              <Button danger onClick={() => store.removeComponent(selected.id)}>删除组件</Button>
            </Form>
          )}
        </Layout.Sider>
      </Layout>
    </Layout>
  )
}
