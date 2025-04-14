import React, { useState } from "react";
import styled, { keyframes } from "styled-components";
import { theme } from "../styles/theme";
import {
  FaTrophy,
  FaStar,
  FaMedal,
  FaCalendarCheck,
  FaChalkboardTeacher,
  FaUser,
  FaExternalLinkAlt,
  FaUserCircle,
} from "react-icons/fa";

const fadeInUp = keyframes`
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: ${theme.spacing.xl};
  background-color: ${theme.colors.background};
`;

const Header = styled.div`
  text-align: center;
  margin-bottom: ${theme.spacing.xxl};
  padding: ${theme.spacing.xl} 0;
`;

const Title = styled.h1`
  font-size: 2.8rem;
  color: ${theme.colors.primary};
  margin-bottom: ${theme.spacing.lg};
  font-weight: 700;
`;

const Subtitle = styled.p`
  font-size: 1.1rem;
  color: ${theme.colors.text};
  margin-bottom: ${theme.spacing.xl};
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
`;

const FilterContainer = styled.div`
  background-color: ${theme.colors.white};
  padding: ${theme.spacing.lg};
  border-radius: ${theme.borderRadius.lg};
  box-shadow: ${theme.shadows.md};
  margin-bottom: ${theme.spacing.xl};
`;

const FilterGroup = styled.div`
  display: flex;
  gap: ${theme.spacing.sm};
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: ${theme.spacing.md};

  &:last-child {
    margin-bottom: 0;
  }
`;

const FilterLabel = styled.span`
  font-weight: 600;
  color: ${theme.colors.text};
  margin-right: ${theme.spacing.md};
  align-self: center;
`;

const FilterButton = styled.button`
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  border: 1px solid ${theme.colors.border};
  border-radius: ${theme.borderRadius.full};
  background-color: ${theme.colors.white};
  color: ${theme.colors.text};
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 0.9rem;

  ${(props) =>
    props.active &&
    `
    background-color: ${theme.colors.primary};
    color: ${theme.colors.white};
    border-color: ${theme.colors.primary};
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  `}

  &:hover:not(:disabled) {
    background-color: ${theme.colors.lightGray};
    border-color: ${theme.colors.gray};
    transform: translateY(-2px);
  }

  ${(props) =>
    props.active &&
    `
    &:hover {
      background-color: ${theme.colors.secondary};
      border-color: ${theme.colors.secondary};
    }
  `}
`;

const StudentGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: ${theme.spacing.xl};
  margin-top: ${theme.spacing.xl};
`;

const StudentCard = styled.div`
  border: 1px solid ${theme.colors.border};
  border-radius: ${theme.borderRadius.xl};
  padding: ${theme.spacing.lg};
  background-color: ${theme.colors.white};
  transition: ${theme.transitions.default};
  box-shadow: ${theme.shadows.sm};
  display: flex;
  flex-direction: column;
  animation: ${fadeInUp} 0.5s ease-out forwards;
  opacity: 0;

  &:hover {
    transform: translateY(-6px);
    box-shadow: ${theme.shadows.lg};
  }
`;

const StudentProfile = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: ${theme.spacing.lg};
`;

const ProfileIconContainer = styled.div`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin-right: ${theme.spacing.md};
  background-color: ${theme.colors.lightGray};
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border: 2px solid ${theme.colors.primary}30;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  svg {
    width: 30px;
    height: 30px;
    color: ${theme.colors.gray};
  }
`;

const StudentName = styled.h3`
  font-size: 1.3rem;
  color: ${theme.colors.text};
  margin-bottom: ${theme.spacing.xxs};
  font-weight: 600;
`;

const StudentInfo = styled.p`
  color: ${theme.colors.gray};
  margin-bottom: 0;
  font-size: 0.9rem;
`;

const SectionDivider = styled.hr`
  border: none;
  border-top: 1px solid ${theme.colors.border};
  margin: ${theme.spacing.lg} 0;
`;

const Skills = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: ${theme.spacing.sm};
  margin-bottom: ${theme.spacing.md};
`;

const SkillTag = styled.span`
  background-color: ${theme.colors.primary}1A;
  padding: ${theme.spacing.xs} ${theme.spacing.md};
  border-radius: ${theme.borderRadius.md};
  font-size: 0.85rem;
  color: ${theme.colors.primary};
  font-weight: 500;
  transition: ${theme.transitions.fast};

  &:hover {
    background-color: ${theme.colors.primary};
    color: ${theme.colors.white};
    transform: scale(1.05);
  }
`;

const Badge = styled.span`
  display: inline-flex;
  align-items: center;
  padding: ${theme.spacing.xs} ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.sm};
  font-size: 0.8rem;
  font-weight: 600;
  margin-right: ${theme.spacing.xs};
  margin-bottom: ${theme.spacing.xs};
  border: 1px solid;
  background-color: transparent;

  ${(props) => {
    let color = theme.colors.gray;
    switch (props.type) {
      case "grand":
        color = theme.colors.gold;
        break;
      case "excellent":
        color = theme.colors.secondary;
        break;
      case "good":
        color = theme.colors.primary;
        break;
      case "attendance":
        color = theme.colors.success;
        break;
      case "tutor":
        color = theme.colors.info;
        break;
    }
    return `
      color: ${color};
      border-color: ${color}80;
    `;
  }}

  svg {
    margin-right: ${theme.spacing.xxs};
    font-size: 1em;
  }
`;

const PortfolioLink = styled.a`
  color: ${theme.colors.primary};
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: ${theme.spacing.xs};
  margin-top: auto;
  padding-top: ${theme.spacing.md};
  font-weight: 500;
  transition: ${theme.transitions.fast};

  &:hover {
    color: ${theme.colors.secondary};
    text-decoration: underline;
    svg {
      transform: translateX(2px);
    }
  }

  svg {
    transition: transform 0.2s ease;
  }
`;

const PortfolioPreview = styled.div`
  margin-top: ${theme.spacing.md};
  border: 1px solid ${theme.colors.border};
  border-radius: ${theme.borderRadius.lg};
  padding: ${theme.spacing.md};
  background-color: ${theme.colors.background};
  transition: ${theme.transitions.default};
  margin-bottom: ${theme.spacing.md};

  &:hover {
    border-color: ${theme.colors.primary};
    box-shadow: ${theme.shadows.sm};
  }
`;

const ProjectTitle = styled.h4`
  font-size: 1rem;
  color: ${theme.colors.text};
  margin-bottom: ${theme.spacing.xs};
  font-weight: 600;
`;

const ProjectDescription = styled.p`
  font-size: 0.9rem;
  color: ${theme.colors.gray};
  margin-bottom: ${theme.spacing.sm};
  line-height: 1.5;
`;

const ProjectImage = styled.img`
  width: 100%;
  border-radius: ${theme.borderRadius.md};
  margin-top: ${theme.spacing.sm};
  aspect-ratio: 16 / 9;
  object-fit: cover;
  border: 1px solid ${theme.colors.border};
`;

const ConnectButton = styled.button`
  background: linear-gradient(
    90deg,
    ${theme.colors.primary},
    ${theme.colors.secondary}
  );
  color: ${theme.colors.white};
  padding: ${theme.spacing.sm} ${theme.spacing.lg};
  border: none;
  border-radius: ${theme.borderRadius.md};
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-top: ${theme.spacing.lg};
  width: 100%;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);

  &:hover:not(:disabled) {
    background: linear-gradient(
      90deg,
      ${theme.colors.secondary},
      ${theme.colors.primary}
    );
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }

  &:disabled {
    background: ${theme.colors.lightGray};
    color: ${theme.colors.gray};
    cursor: not-allowed;
  }
`;

const ProfileIcon = styled(FaUserCircle)`
  width: 60px;
  height: 60px;
  margin-right: ${theme.spacing.md};
  color: ${theme.colors.primary};
`;

const getBadgeIcon = (type) => {
  switch (type) {
    case "grand":
      return <FaTrophy />;
    case "excellent":
      return <FaStar />;
    case "good":
      return <FaMedal />;
    case "attendance":
      return <FaCalendarCheck />;
    case "tutor":
      return <FaChalkboardTeacher />;
    default:
      return null;
  }
};

const getBadgeText = (type) => {
  switch (type) {
    case "grand":
      return "프로젝트 대상";
    case "excellent":
      return "최우수상";
    case "good":
      return "우수상";
    case "attendance":
      return "개근상";
    case "tutor":
      return "튜터";
    default:
      return type;
  }
};

const CompanyServicePage = () => {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedFilter, setSelectedFilter] = useState("recent");

  const categories = [
    "all",
    "UI/UX",
    "데이터분석",
    "앱개발",
    "프론트엔드",
    "백엔드",
    "클라우드 엔지니어링",
    "그로스 마케터",
    "블록체인",
  ];

  const filters = ["recent", "popular", "recommended"];

  const students = [
    {
      id: 1,
      name: "김수료",
      profileImage: "https://randomuser.me/api/portraits/women/1.jpg",
      course: "KDT 프론트엔드 1기",
      school: "서울대학교",
      skills: ["React", "JavaScript", "HTML", "CSS", "TypeScript", "Next.js"],
      portfolio: "https://example.com/portfolio",
      badges: ["grand", "tutor"],
      projects: [
        {
          title: "쇼핑몰 웹사이트",
          description: "React와 Node.js를 사용한 풀스택 프로젝트",
          image: "https://via.placeholder.com/300x169",
        },
      ],
    },
    {
      id: 2,
      name: "이개발",
      profileImage: "https://randomuser.me/api/portraits/men/2.jpg",
      course: "KDT 백엔드 2기",
      school: "연세대학교",
      skills: ["Java", "Spring Boot", "MySQL", "Docker", "AWS"],
      portfolio: "https://example.com/portfolio2",
      badges: ["excellent", "attendance"],
      projects: [
        {
          title: "API 게이트웨이 서비스",
          description: "Spring Cloud Gateway를 활용한 마이크로서비스 아키텍처",
          image: "https://via.placeholder.com/300x169",
        },
      ],
    },
    {
      id: 3,
      name: "박디자인",
      profileImage: "https://randomuser.me/api/portraits/women/3.jpg",
      course: "KDT UI/UX 1기",
      school: "고려대학교",
      skills: [
        "Figma",
        "Adobe XD",
        "Photoshop",
        "Illustrator",
        "After Effects",
      ],
      portfolio: "https://example.com/portfolio3",
      badges: ["good", "tutor"],
      projects: [
        {
          title: "모바일 앱 UI/UX 리디자인",
          description: "사용자 경험 개선을 위한 앱 리디자인 프로젝트",
          image: "https://via.placeholder.com/300x200",
        },
      ],
    },
    {
      id: 4,
      name: "정데이터",
      profileImage: "https://randomuser.me/api/portraits/men/4.jpg",
      course: "KDT 데이터분석 2기",
      school: "한양대학교",
      skills: ["Python", "Pandas", "TensorFlow", "SQL", "Tableau"],
      portfolio: "https://example.com/portfolio4",
      badges: ["grand", "excellent"],
      projects: [
        {
          title: "고객 행동 예측 모델",
          description: "머신러닝을 활용한 고객 구매 패턴 분석",
          image: "https://via.placeholder.com/300x200",
        },
      ],
    },
    {
      id: 5,
      name: "최앱개발",
      profileImage: "https://randomuser.me/api/portraits/women/5.jpg",
      course: "KDT 앱개발 1기",
      school: "성균관대학교",
      skills: ["React Native", "Flutter", "Firebase", "Redux", "GraphQL"],
      portfolio: "https://example.com/portfolio5",
      badges: ["excellent", "attendance"],
      projects: [
        {
          title: "헬스케어 모바일 앱",
          description: "React Native로 개발한 건강 관리 앱",
          image: "https://via.placeholder.com/300x200",
        },
      ],
    },
    {
      id: 6,
      name: "강클라우드",
      profileImage: "https://randomuser.me/api/portraits/men/6.jpg",
      course: "KDT 클라우드 엔지니어링 1기",
      school: "경희대학교",
      skills: ["AWS", "Kubernetes", "Terraform", "Docker", "CI/CD"],
      portfolio: "https://example.com/portfolio6",
      badges: ["good", "tutor"],
      projects: [
        {
          title: "클라우드 인프라 구축",
          description: "AWS를 활용한 마이크로서비스 아키텍처 구축",
          image: "https://via.placeholder.com/300x200",
        },
      ],
    },
    {
      id: 7,
      name: "윤마케터",
      profileImage: "https://randomuser.me/api/portraits/women/7.jpg",
      course: "KDT 그로스 마케터 1기",
      school: "서강대학교",
      skills: [
        "Google Analytics",
        "SEO",
        "Content Marketing",
        "Social Media",
        "Data Analysis",
      ],
      portfolio: "https://example.com/portfolio7",
      badges: ["excellent", "attendance"],
      projects: [
        {
          title: "바이럴 마케팅 캠페인",
          description: "소셜 미디어를 활용한 성공적인 마케팅 캠페인",
          image: "https://via.placeholder.com/300x200",
        },
      ],
    },
    {
      id: 8,
      name: "장블록체인",
      profileImage: "https://randomuser.me/api/portraits/men/8.jpg",
      course: "KDT 블록체인 1기",
      school: "숭실대학교",
      skills: ["Solidity", "Ethereum", "Web3.js", "Smart Contracts", "DeFi"],
      portfolio: "https://example.com/portfolio8",
      badges: ["grand", "tutor"],
      projects: [
        {
          title: "NFT 마켓플레이스",
          description: "이더리움 기반 NFT 거래 플랫폼",
          image: "https://via.placeholder.com/300x200",
        },
      ],
    },
    {
      id: 9,
      name: "한프론트",
      profileImage: "https://randomuser.me/api/portraits/women/9.jpg",
      course: "KDT 프론트엔드 2기",
      school: "홍익대학교",
      skills: ["Vue.js", "Nuxt.js", "Tailwind CSS", "GraphQL", "Jest"],
      portfolio: "https://example.com/portfolio9",
      badges: ["good", "attendance"],
      projects: [
        {
          title: "실시간 채팅 웹앱",
          description: "Vue.js와 Socket.io를 활용한 실시간 채팅 서비스",
          image: "https://via.placeholder.com/300x200",
        },
      ],
    },
    {
      id: 10,
      name: "서백엔드",
      profileImage: "https://randomuser.me/api/portraits/men/10.jpg",
      course: "KDT 백엔드 1기",
      school: "중앙대학교",
      skills: ["Node.js", "Express", "MongoDB", "Redis", "GraphQL"],
      portfolio: "https://example.com/portfolio10",
      badges: ["excellent", "tutor"],
      projects: [
        {
          title: "실시간 알림 시스템",
          description: "WebSocket을 활용한 실시간 알림 서비스",
          image: "https://via.placeholder.com/300x169",
        },
      ],
    },
  ];

  const handleConnect = (studentId) => {
    alert(`학생 ID ${studentId}에게 연락처 공유 요청이 전송되었습니다.`);
  };

  const filteredStudents = students;

  return (
    <Container>
      <Header>
        <Title>KDT 수료생 포트폴리오</Title>
        <Subtitle>
          엄선된 KDT 수료생들의 혁신적인 프로젝트와 잠재력을 확인하고,
          <br />
          기업의 성장을 이끌 인재를 만나보세요.
        </Subtitle>
      </Header>

      <FilterContainer>
        <FilterGroup>
          <FilterLabel>카테고리:</FilterLabel>
          {categories.map((category) => (
            <FilterButton
              key={category}
              active={selectedCategory === category}
              onClick={() => setSelectedCategory(category)}
            >
              {category === "all" ? "전체" : category}
            </FilterButton>
          ))}
        </FilterGroup>
        <FilterGroup>
          <FilterLabel>정렬:</FilterLabel>
          {filters.map((filter) => (
            <FilterButton
              key={filter}
              active={selectedFilter === filter}
              onClick={() => setSelectedFilter(filter)}
            >
              {filter === "recent"
                ? "최신순"
                : filter === "popular"
                ? "인기순"
                : "추천순"}
            </FilterButton>
          ))}
        </FilterGroup>
      </FilterContainer>

      <StudentGrid>
        {filteredStudents.map((student, index) => (
          <StudentCard
            key={student.id}
            style={{ animationDelay: `${index * 0.05}s` }}
          >
            <StudentProfile>
              <ProfileIconContainer>
                {student.profileImage ? (
                  <img
                    src={student.profileImage}
                    alt={`${student.name} 프로필`}
                  />
                ) : (
                  <ProfileIcon />
                )}
              </ProfileIconContainer>
              <div>
                <StudentName>{student.name}</StudentName>
                <StudentInfo>{student.school}</StudentInfo>
                <StudentInfo>{student.course}</StudentInfo>
              </div>
            </StudentProfile>

            {student.badges && student.badges.length > 0 && (
              <>
                <Skills>
                  {student.badges.map((badge, index) => (
                    <Badge key={index} type={badge}>
                      {getBadgeIcon(badge)}
                      {getBadgeText(badge)}
                    </Badge>
                  ))}
                </Skills>
                <SectionDivider />
              </>
            )}

            <Skills>
              {student.skills.map((skill) => (
                <SkillTag key={skill}>{skill}</SkillTag>
              ))}
            </Skills>

            {student.projects && student.projects.length > 0 && (
              <>
                <SectionDivider />
                {student.projects.map((project, index) => (
                  <PortfolioPreview key={index}>
                    <ProjectTitle>{project.title}</ProjectTitle>
                    <ProjectDescription>
                      {project.description}
                    </ProjectDescription>
                    {project.image && (
                      <ProjectImage src={project.image} alt={project.title} />
                    )}
                  </PortfolioPreview>
                ))}
              </>
            )}

            <PortfolioLink
              href={student.portfolio}
              target="_blank"
              rel="noopener noreferrer"
            >
              전체 포트폴리오 보기 <FaExternalLinkAlt size="0.8em" />
            </PortfolioLink>

            <ConnectButton onClick={() => handleConnect(student.id)}>
              🚀 커넥트 요청
            </ConnectButton>
          </StudentCard>
        ))}
      </StudentGrid>
    </Container>
  );
};

export default CompanyServicePage;
