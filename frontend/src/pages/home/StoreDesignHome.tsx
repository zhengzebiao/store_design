import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { App, Button, Card, Col, Empty, Form, Input, Pagination, Popconfirm, Row, Select, Space, Spin, Tag, Typography } from 'antd'
import { getErrorMessage } from '../../api/error'
import { deleteTemplate, getTemplates, useTemplate } from '../../api/templates'
import type { StoreTemplate, TemplateListParams } from '../../domain/template'
import './home.less'

const COMPANY_ID = 3
const DEFAULT_PARAMS: TemplateListParams = {
  page: 1,
  limit: 20,
  company_id: COMPANY_ID,
  type: 'diy',
}

export default function StoreDesignHome() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { message } = App.useApp()
  const [params, setParams] = useState(DEFAULT_PARAMS)
  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ['templates', params],
    queryFn: () => getTemplates(params),
  })

  const refreshTemplates = () => queryClient.invalidateQueries({ queryKey: ['templates'] })
  const useTemplateMutation = useMutation({
    mutationFn: (template: StoreTemplate) => useTemplate(template.id, COMPANY_ID),
    onSuccess: () => {
      message.success('使用模板成功')
      refreshTemplates()
    },
    onError: (mutationError) => {
      message.error(getErrorMessage(mutationError, '使用模板失败'))
    },
  })
  const deleteTemplateMutation = useMutation({
    mutationFn: (template: StoreTemplate) => deleteTemplate(template.id, COMPANY_ID),
    onSuccess: () => {
      message.success('删除模板成功')
      refreshTemplates()
    },
    onError: (mutationError) => {
      message.error(getErrorMessage(mutationError, '删除模板失败'))
    },
  })

  const templates = data?.data || []

  return (
    <main className="store-home">
      <section className="store-home__header">
        <div>
          <Typography.Title level={3}>店铺装修</Typography.Title>
          <Typography.Text type="secondary">管理模板选择、创建、编辑和保存流程</Typography.Text>
        </div>
        <Space>
          <Button onClick={() => refetch()}>刷新数据</Button>
          <Button type="primary" onClick={() => navigate('/edit?mode=create')}>新建装修</Button>
        </Space>
      </section>

      <Card className="store-home__filters">
        <Form
          layout="inline"
          initialValues={params}
          onFinish={(values) => setParams({ ...DEFAULT_PARAMS, ...values, page: 1 })}
        >
          <Form.Item name="keyword" label="关键词">
            <Input allowClear placeholder="模板名称" />
          </Form.Item>
          <Form.Item name="type" label="模板类型">
            <Select style={{ width: 140 }} options={[{ label: 'diy', value: 'diy' }]} />
          </Form.Item>
          <Form.Item name="is_sel" label="使用状态">
            <Select
              allowClear
              style={{ width: 140 }}
              options={[{ label: '使用中', value: 1 }, { label: '未使用', value: 0 }]}
            />
          </Form.Item>
          <Form.Item>
            <Button htmlType="submit" type="primary">查询</Button>
          </Form.Item>
        </Form>
      </Card>

      {isLoading && <Spin className="store-home__state" />}
      {isError && (
        <Empty className="store-home__state" description={(error as Error).message || '模板加载失败'}>
          <Button onClick={() => refetch()}>重试</Button>
        </Empty>
      )}
      {!isLoading && !isError && templates.length === 0 && <Empty className="store-home__state" description="暂无模板" />}

      <Row gutter={[16, 16]}>
        {templates.map((template) => (
          <Col key={template.id} xs={24} sm={12} lg={8} xl={6}>
            <Card
              hoverable
              cover={template.head_img ? <img alt={template.name} src={template.head_img} /> : undefined}
              actions={[
                <Button type="link" onClick={() => navigate(`/edit?mode=edit&id=${template.id}`)}>编辑</Button>,
                <Button type="link" onClick={() => navigate(`/edit?mode=copy&id=${template.id}`)}>复制</Button>,
                <Button
                  type="link"
                  disabled={template.is_sel === 1}
                  loading={useTemplateMutation.isPending && useTemplateMutation.variables?.id === template.id}
                  onClick={() => useTemplateMutation.mutate(template)}
                >
                  使用模板
                </Button>,
                <Popconfirm
                  title="确认删除该模板？"
                  description="删除后将无法在列表中继续编辑。"
                  okText="删除"
                  cancelText="取消"
                  disabled={template.system_recommend_template === 1}
                  onConfirm={() => deleteTemplateMutation.mutate(template)}
                >
                  <Button
                    danger
                    type="link"
                    disabled={template.system_recommend_template === 1}
                    loading={deleteTemplateMutation.isPending && deleteTemplateMutation.variables?.id === template.id}
                  >
                    删除
                  </Button>
                </Popconfirm>,
              ]}
            >
              <Card.Meta title={template.name} description={`ID: ${template.id}`} />
              <Space className="store-home__tags" wrap>
                <Tag color={template.is_sel ? 'green' : 'default'}>{template.is_sel ? '使用中' : '未使用'}</Tag>
                <Tag>{template.type}</Tag>
                {template.system_recommend_template ? <Tag color="blue">系统推荐</Tag> : null}
              </Space>
            </Card>
          </Col>
        ))}
      </Row>

      {data && data.total > 0 && (
        <Pagination
          className="store-home__pagination"
          current={data.current_page}
          pageSize={data.limit}
          total={data.total}
          showSizeChanger
          showTotal={(total) => `共 ${total} 条`}
          onChange={(page, limit) => setParams((current) => ({ ...current, page, limit }))}
        />
      )}
    </main>
  )
}
