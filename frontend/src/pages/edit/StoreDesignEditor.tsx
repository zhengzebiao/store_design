import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { App, Button, Card, Empty, Form, Input, Layout, List, Space, Spin, Typography } from 'antd'
import { getComponents } from '../../api/components'
import { getTemplateDetail } from '../../api/templates'
import { savePage } from '../../api/pages'
import { createComponentFromMeta, createEmptyPage } from '../../domain/factory'
import { useEditorStore } from '../../store/editorStore'
import './editor.less'

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
          <Button
            type="primary"
            loading={saveMutation.isPending}
            onClick={() => saveMutation.mutate({ ...page, mode, route_id: routeId })}
          >
            保存
          </Button>
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

        <Layout.Sider width={320} theme="light" className="store-editor__panel">
          <Typography.Title level={5}>配置面板</Typography.Title>
          {!selected && (
            <Form layout="vertical">
              <Form.Item label="页面名称">
                <Input value={page.page_name} onChange={(event) => store.updatePageName(event.target.value)} />
              </Form.Item>
            </Form>
          )}
          {selected && (
            <Form layout="vertical">
              <Form.Item label="组件标题">
                <Input value={selected.component_title} onChange={(event) => store.updateSelectedTitle(event.target.value)} />
              </Form.Item>
              <Form.Item label="调试数据">
                <Input.TextArea value={JSON.stringify(selected.remote_data, null, 2)} rows={8} readOnly />
              </Form.Item>
              <Button danger onClick={() => store.removeComponent(selected.id)}>删除组件</Button>
            </Form>
          )}
        </Layout.Sider>
      </Layout>
    </Layout>
  )
}
