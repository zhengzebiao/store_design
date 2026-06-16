import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { App, Button, Card, Col, Empty, Form, Input, Row, Select, Space, Spin, Tag, Typography } from 'antd'
import { getTemplates } from '../../api/templates'
import type { TemplateListParams } from '../../domain/template'
import './home.less'

const DEFAULT_PARAMS: TemplateListParams = {
  page: 1,
  limit: 20,
  type: 'diy',
}

export default function StoreDesignHome() {
  const navigate = useNavigate()
  const { message } = App.useApp()
  const [params, setParams] = useState(DEFAULT_PARAMS)
  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ['templates', params],
    queryFn: () => getTemplates(params),
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

      {data && data.total > data.limit && (
        <Button className="store-home__more" onClick={() => message.info('分页组件将在下一阶段接入')}>
          共 {data.total} 条
        </Button>
      )}
    </main>
  )
}
